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
    throw "No se encontró el comando '$cmd'."
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
    Write-Section "Levantando servicios (payment-service + partner-php + ai-orchestrator)"
    docker compose -f $ComposeFile up -d --build payment-service partner-php ai-orchestrator | Out-Host
  } else {
    Write-Host "SkipCompose: asumiendo servicios ya levantados." -ForegroundColor Yellow
  }

  Write-Section "Esperando health checks"
  Wait-HttpOk "http://localhost:8002/health"
  Wait-HttpOk "http://localhost:8088/health"
  Wait-HttpOk "http://localhost:8003/health"

  Write-Section "Tool: info (ai-orchestrator /chat)"
  $info = Invoke-RestMethod -Uri "http://localhost:8003/chat" -Method POST -ContentType "application/json" -Body (
    @{ message = "info"; toolName = "info"; toolArgs = @{} } | ConvertTo-Json -Depth 8
  )
  if (-not $info.toolsUsed -or $info.toolsUsed[0].tool -ne "info") {
    throw "info falló: $($info | ConvertTo-Json -Depth 20)"
  }

  Write-Section "Registrar partner (para activar_service -> webhook al PHP)"
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

  Write-Section "Recrear partner-php con PARTNER_ID + PARTNER_SHARED_SECRET"
  $env:PARTNER_ID = $partnerId
  $env:PARTNER_SHARED_SECRET = $secret
  $env:TARGET_URL = "http://payment-service:8002/webhooks/partner"

  docker compose -f $ComposeFile up -d --force-recreate partner-php | Out-Host
  Wait-HttpOk "http://localhost:8088/health"

  Write-Section "Tool: create_payment (ai-orchestrator /chat)"
  $create = Invoke-RestMethod -Uri "http://localhost:8003/chat" -Method POST -ContentType "application/json" -Body (
    @{ message = "crea un pago"; toolName = "create_payment"; toolArgs = @{ amount = 12.34; currency = "USD"; metadata = @{ source = "smoke" } } } | ConvertTo-Json -Depth 8
  )

  $paymentId = [string]$create.toolsUsed[0].result.payment.id
  if ([string]::IsNullOrWhiteSpace($paymentId)) {
    throw "No se obtuvo payment.id desde create_payment. Respuesta: $($create | ConvertTo-Json -Depth 20)"
  }
  Write-Host "paymentId: $paymentId" -ForegroundColor Green

  Write-Section "Tool: query_payment"
  $query = Invoke-RestMethod -Uri "http://localhost:8003/chat" -Method POST -ContentType "application/json" -Body (
    @{ message = "consulta pago"; toolName = "query_payment"; toolArgs = @{ payment_id = $paymentId } } | ConvertTo-Json -Depth 8
  )
  if (-not $query.toolsUsed[0].result.ok) {
    throw "query_payment falló: $($query | ConvertTo-Json -Depth 20)"
  }

  Write-Section "Tool: report"
  $report = Invoke-RestMethod -Uri "http://localhost:8003/chat" -Method POST -ContentType "application/json" -Body (
    @{ message = "reporte"; toolName = "report"; toolArgs = @{} } | ConvertTo-Json -Depth 8
  )
  if (-not $report.toolsUsed[0].result.ok) {
    throw "report falló: $($report | ConvertTo-Json -Depth 20)"
  }
  Write-Host ("total_pagos: {0}, monto_total: {1}" -f $report.toolsUsed[0].result.total_pagos, $report.toolsUsed[0].result.monto_total) -ForegroundColor Green

  Write-Section "Tool: activate_service (ai-orchestrator -> payment-service -> partner-php)"
  $activate = Invoke-RestMethod -Uri "http://localhost:8003/chat" -Method POST -ContentType "application/json" -Body (
    @{ message = "activa"; toolName = "activate_service"; toolArgs = @{ partner_id = $partnerId; servicio = "pagos" } } | ConvertTo-Json -Depth 8
  )

  $down = $activate.toolsUsed[0].result.downstream.downstream.status_code
  Write-Host ("activate_service downstream.status_code: {0}" -f $down) -ForegroundColor Green
  if ($down -ne 200) {
    throw "activate_service no llegó OK al PHP. Respuesta: $($activate | ConvertTo-Json -Depth 20)"
  }

  Write-Section "RESULTADO"
  Write-Host "✅ Smoke test OK: 5 tools probadas + webhook al backend PHP" -ForegroundColor Green

} finally {
  Pop-Location
}
