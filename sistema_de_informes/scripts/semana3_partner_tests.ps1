param(
  [switch]$SkipCompose,
  [string]$ComposeFile = "docker-compose.yml"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Section([string]$msg) {
  Write-Host "\n=== $msg ===" -ForegroundColor Cyan
}

function Assert-Command([string]$cmd) {
  $exists = Get-Command $cmd -ErrorAction SilentlyContinue
  if (-not $exists) {
    throw "No se encontró el comando '$cmd'. Instala Docker Desktop y asegúrate que 'docker' esté en PATH."
  }
}

function Wait-HttpOk([string]$url, [int]$retries = 30, [int]$delaySeconds = 2) {
  for ($i = 1; $i -le $retries; $i++) {
    try {
      $r = Invoke-WebRequest -Uri $url -Method GET -TimeoutSec 3
      if ($r.StatusCode -eq 200) { return }
    } catch {
      Start-Sleep -Seconds $delaySeconds
    }
  }
  throw "No respondió OK: $url"
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Push-Location $repoRoot

try {
  Write-Section "Prechecks"
  Assert-Command docker

  if (-not $SkipCompose) {
    Write-Section "Levantando servicios (payment-service + partner-php)"
    # Levanta solo lo necesario para Semana 3
    docker compose -f $ComposeFile up -d --build payment-service partner-php | Out-Host
  } else {
    Write-Host "SkipCompose: asumiendo servicios ya levantados." -ForegroundColor Yellow
  }

  Write-Section "Esperando health checks"
  Wait-HttpOk "http://localhost:8002/health"
  Wait-HttpOk "http://localhost:8088/health"

  Write-Section "Registrar partner en payment-service (/partners/register)"
  $registerBody = @{
    name      = "partner-php"
    webhookUrl = "http://partner-php/partner/webhook"
    events    = @("tour.purchased","payment.success")
  } | ConvertTo-Json -Depth 5

  $registerResp = Invoke-RestMethod -Uri "http://localhost:8002/partners/register" -Method POST -ContentType "application/json" -Body $registerBody

  $partnerId = [string]$registerResp.partnerId
  $secret    = [string]$registerResp.secret

  if ([string]::IsNullOrWhiteSpace($partnerId) -or [string]::IsNullOrWhiteSpace($secret)) {
    throw "Registro de partner no devolvió partnerId/secret. Respuesta: $($registerResp | ConvertTo-Json -Depth 10)"
  }

  Write-Host "partnerId: $partnerId" -ForegroundColor Green
  Write-Host "secret:    (oculto)" -ForegroundColor Green

  Write-Section "Recrear partner-php con env vars (PARTNER_ID + PARTNER_SHARED_SECRET + TARGET_URL)"
  $env:PARTNER_ID = $partnerId
  $env:PARTNER_SHARED_SECRET = $secret
  $env:TARGET_URL = "http://payment-service:8002/webhooks/partner"

  # Recreate para inyectar variables de entorno
  docker compose -f $ComposeFile up -d --force-recreate partner-php | Out-Host

  Wait-HttpOk "http://localhost:8088/health"

  Write-Section "Prueba dirección B: partner -> sistema (POST /partner/trigger)"
  $triggerResp = Invoke-RestMethod -Uri "http://localhost:8088/partner/trigger" -Method POST -ContentType "application/json" -Body "{}"

  $downStatus = $triggerResp.downstream.status_code
  Write-Host ("Downstream status_code: {0}" -f $downStatus) -ForegroundColor Green

  if ($downStatus -ne 200) {
    throw "Fallo partner->sistema. Respuesta: $($triggerResp | ConvertTo-Json -Depth 20)"
  }

  Write-Section "Prueba dirección A: sistema -> partner (POST /partners/{id}/send-test)"
  $sendTestResp = Invoke-RestMethod -Uri "http://localhost:8002/partners/$partnerId/send-test" -Method POST -ContentType "application/json" -Body "{}"
  $sendDown = $sendTestResp.downstream.status_code
  Write-Host ("Downstream status_code: {0}" -f $sendDown) -ForegroundColor Green

  if ($sendDown -ne 200) {
    throw "Fallo sistema->partner. Respuesta: $($sendTestResp | ConvertTo-Json -Depth 20)"
  }

  Write-Section "Prueba negativa HMAC (firma inválida => 401)"
  $badBody = '{"event":"test.bad","data":{},"timestamp":"2026-01-15T00:00:00Z","source":"our-system"}'
  try {
    Invoke-WebRequest -Uri "http://localhost:8088/partner/webhook" -Method POST -ContentType "application/json" -Headers @{"X-Signature"="deadbeef"} -Body $badBody | Out-Null
    throw "Se esperaba 401 pero el endpoint respondió OK"
  } catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -ne 401) {
      throw "Se esperaba 401 y llegó $statusCode"
    }
    Write-Host "OK: recibió 401 como se esperaba" -ForegroundColor Green
  }

  Write-Section "RESULTADO"
  Write-Host "✅ Semana 3 - Pruebas B2B completadas: bidireccional + HMAC OK" -ForegroundColor Green
  Write-Host "- partnerId: $partnerId" -ForegroundColor Gray
  Write-Host "- TARGET_URL: $env:TARGET_URL" -ForegroundColor Gray

} finally {
  Pop-Location
}
