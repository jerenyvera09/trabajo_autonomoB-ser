# PowerShell - Demo Semana 5 (Segundo Parcial)
# Objetivo: demo reproducible para la presentación.
# Flujo sugerido:
#   n8n Payment Handler -> Payment Service -> REST integrations (WS + Email) -> Partner webhook
# Evidencias:
#   - MailHog recibe email
#   - Webhook de n8n responde 200 (si workflow está ACTIVO)

$restApi = "http://localhost:8000"
$paymentService = "http://localhost:8002"
$n8n = "http://localhost:5679"
$mailhog = "http://localhost:8025"
$ws = "http://localhost:8080"

$partnerId = "partner_php_demo"
$sharedSecret = "dev-partner-secret-change-me"

Write-Host "[0] Health checks..."
Invoke-RestMethod -Uri "$restApi/health" -Method Get | Out-Null
Invoke-RestMethod -Uri "$paymentService/health" -Method Get | Out-Null
Invoke-RestMethod -Uri "$ws/health" -Method Get | Out-Null

Write-Host "[1] Registrar partner estable en Payment Service (si ya existe, es OK)..."
$registerBody = @{
  name = "partner-php"
  webhookUrl = "http://partner-php/partner/webhook"
  events = @("payment.success")
  partnerId = $partnerId
  secret = $sharedSecret
} | ConvertTo-Json

try {
  $reg = Invoke-RestMethod -Uri "$paymentService/partners/register" -Method Post -Body $registerBody -ContentType "application/json"
  Write-Host "Partner registrado: $($reg.partnerId)"
} catch {
  Write-Host "Aviso: register pudo fallar si ya existía (OK). Detalle: $($_.Exception.Message)"
}

Write-Host "[2] Disparar webhook Payment Handler en n8n..."
Write-Host "  Nota: si recibes 404 \"webhook not registered\", debes ACTIVAR el workflow en n8n UI (http://localhost:5679)"

$payload = @{
  amount = 12.5
  currency = "USD"
  partnerId = $partnerId
  email = "demo@local.test"
} | ConvertTo-Json

try {
  $resp = Invoke-RestMethod -Uri "$n8n/webhook/payment-handler" -Method Post -Body $payload -ContentType "application/json"
  Write-Host "Respuesta n8n (ok):"
  Write-Host ($resp | ConvertTo-Json -Depth 10)
} catch {
  Write-Host "ERROR llamando a n8n: $($_.Exception.Message)"
  Write-Host "Abre n8n -> Workflows -> activa Payment Handler y reintenta."
  exit 1
}

Start-Sleep -Seconds 2

Write-Host "[3] Verificar email en MailHog (API)..."
try {
  $msgs = Invoke-RestMethod -Uri "$mailhog/api/v2/messages" -Method Get
  $count = [int]$msgs.count
  Write-Host "MailHog mensajes: $count"
  if ($count -gt 0) {
    $latest = $msgs.items[0]
    Write-Host "Ultimo asunto: $($latest.Content.Headers.Subject[0])"
    Write-Host "Ultimo destino: $($latest.Content.Headers.To[0])"
  } else {
    Write-Host "No hay mensajes aún. Abre UI: http://localhost:8025 y revisa."
  }
} catch {
  Write-Host "No pude consultar MailHog API: $($_.Exception.Message)"
}

Write-Host "[OK] Demo Semana 5 terminada."
