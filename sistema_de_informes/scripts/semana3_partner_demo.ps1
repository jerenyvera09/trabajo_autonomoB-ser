Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Wait-HttpOk {
  param(
    [Parameter(Mandatory=$true)][string]$Url,
    [int]$TimeoutSeconds = 60
  )

  $start = Get-Date
  while (((Get-Date) - $start).TotalSeconds -lt $TimeoutSeconds) {
    try {
      $r = Invoke-WebRequest -UseBasicParsing -Uri $Url -Method GET -TimeoutSec 5
      if ($r.StatusCode -ge 200 -and $r.StatusCode -lt 300) { return }
    } catch {
      Start-Sleep -Seconds 2
    }
  }
  throw "Timeout esperando OK en $Url"
}

Write-Host "[Semana3] Levantando payment-service + partner-php..."
# Nota: el compose principal ya incluye partner-php. Si existe backend_php/docker-compose.partner-php.yml, lo incluimos.
$overlay = Join-Path $PSScriptRoot "..\..\backend_php\docker-compose.partner-php.yml"
if (Test-Path $overlay) {
  docker compose -f docker-compose.yml -f $overlay up -d --build payment-service partner-php | Out-Host
} else {
  docker compose up -d --build payment-service partner-php | Out-Host
}

Write-Host "[Semana3] Esperando health..."
Wait-HttpOk -Url "http://localhost:8002/health" -TimeoutSeconds 90
Wait-HttpOk -Url "http://localhost:8088/health" -TimeoutSeconds 90

Write-Host "[Semana3] Registrando partner en payment-service..."
$registerBody = @{
  name = "partner-php"
  webhookUrl = "http://partner-php/partner/webhook"
  events = @("tour.purchased","payment.success")
} | ConvertTo-Json -Depth 5

$reg = Invoke-RestMethod -Uri "http://localhost:8002/partners/register" -Method POST -ContentType "application/json" -Body $registerBody
$partnerId = $reg.partnerId
$secret = $reg.secret
if (-not $partnerId -or -not $secret) { throw "No se obtuvo partnerId/secret desde /partners/register" }

Write-Host "[Semana3] partnerId=$partnerId"

Write-Host "[Semana3] Re-creando partner-php con PARTNER_ID + PARTNER_SHARED_SECRET..."
$env:PARTNER_ID = $partnerId
$env:PARTNER_SHARED_SECRET = $secret
$env:TARGET_URL = "http://payment-service:8002/webhooks/partner"

if (Test-Path $overlay) {
  docker compose -f docker-compose.yml -f $overlay up -d --build --force-recreate partner-php | Out-Host
} else {
  docker compose up -d --build --force-recreate partner-php | Out-Host
}

Wait-HttpOk -Url "http://localhost:8088/health" -TimeoutSeconds 60

Write-Host "[Semana3] Prueba A: nuestro sistema -> partner (send-test)"
$send = Invoke-RestMethod -Uri "http://localhost:8002/partners/$partnerId/send-test" -Method POST
$downA = $send.downstream.status_code
Write-Host "[Semana3] send-test downstream.status_code=$downA"
if ($downA -ne 200) { throw "Fallo Prueba A: esperado 200, recibido $downA" }

Write-Host "[Semana3] Prueba B: partner -> nuestro sistema (/partner/trigger)"
# Nota: el partner corre en 8088 (no 9000) según docker-compose.yml actual.
$trigger = Invoke-RestMethod -Uri "http://localhost:8088/partner/trigger" -Method POST
$downB = $trigger.downstream.status_code
Write-Host "[Semana3] trigger downstream.status_code=$downB"
if ($downB -ne 200) { throw "Fallo Prueba B: esperado 200, recibido $downB" }

Write-Host "[Semana3] OK - Bidireccionalidad + HMAC demostrada (200/200)."
