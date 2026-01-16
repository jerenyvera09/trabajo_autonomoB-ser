# PowerShell - Test de integración Semana 4
# Flujo completo:
#   PDF → REST API (extraer texto) → Chat → MCP Tool → Payment Service → webhook → Partner PHP
#   + validación bidireccional: Partner PHP → Payment Service

$restApi = "http://localhost:8000"
$aiOrchestrator = "http://localhost:8003"
$paymentService = "http://localhost:8002"
$partnerPhp = "http://localhost:8088"

$partnerId = "partner_php_demo"
$sharedSecret = "dev-partner-secret-change-me"

function Ensure-SamplePdf([string]$path) {
    if (Test-Path $path) { return }

    # PDF mínimo válido (con texto) en base64, para que PyPDF2 extraiga contenido.
    $b64 = "JVBERi0xLjQKMSAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZyAvUGFnZXMgMiAwIFIgPj4KZW5kb2JqCjIgMCBvYmoKPDwgL1R5cGUgL1BhZ2VzIC9LaWRzIFszIDAgUl0gL0NvdW50IDEgPj4KZW5kb2JqCjMgMCBvYmoKPDwgL1R5cGUgL1BhZ2UgL1BhcmVudCAyIDAgUiAvTWVkaWFCb3ggWzAgMCAzMDAgMTQ0XSAvUmVzb3VyY2VzIDw8IC9Gb250IDw8IC9GMSA0IDAgUiA+PiA+PiAvQ29udGVudHMgNSAwIFIgPj4KZW5kb2JqCjQgMCBvYmoKPDwgL1R5cGUgL0ZvbnQgL1N1YnR5cGUgL1R5cGUxIC9CYXNlRm9udCAvSGVsdmV0aWNhID4+CmVuZG9iago1IDAgb2JqCjw8IC9MZW5ndGggNDYgPj4Kc3RyZWFtCkJUIC9GMSAxOCBUZiA1MCA5MCBUZCAoVG90YWwgNDIuNTAgVVNEKSBUaiBFVAplbmRzdHJlYW0KZW5kb2JqCnhyZWYKMCA2CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAwOSAwMDAwMCBuIAowMDAwMDAwMDU4IDAwMDAwIG4gCjAwMDAwMDAxMTUgMDAwMDAgbiAKMDAwMDAwMDI0MSAwMDAwMCBuIAowMDAwMDAwMzExIDAwMDAwIG4gCnRyYWlsZXIKPDwgL1NpemUgNiAvUm9vdCAxIDAgUiA+PgpzdGFydHhyZWYKNDA2CiUlRU9GCg=="
    $bytes = [Convert]::FromBase64String($b64)
    [System.IO.File]::WriteAllBytes($path, $bytes)
}

Write-Host "[0] Health checks..."
Invoke-RestMethod -Uri "$restApi/health" -Method Get | Out-Null
Invoke-RestMethod -Uri "$aiOrchestrator/health" -Method Get | Out-Null
Invoke-RestMethod -Uri "$paymentService/health" -Method Get | Out-Null
Invoke-RestMethod -Uri "$partnerPhp/health" -Method Get | Out-Null

Write-Host "[1] Registrando partner estable (id+secret) en Payment Service..."
$registerBody = @{
    name = "partner-php"
    webhookUrl = "http://partner-php/partner/webhook"
    events = @("payment.success", "tour.purchased")
    partnerId = $partnerId
    secret = $sharedSecret
} | ConvertTo-Json

try {
    $reg = Invoke-RestMethod -Uri "$paymentService/partners/register" -Method Post -Body $registerBody -ContentType "application/json"
    Write-Host "Partner registrado: $($reg.partnerId)"
} catch {
    Write-Host "Aviso: register pudo fallar si ya existía (OK). Detalle: $($_.Exception.Message)"
}

Write-Host "[2] Subiendo PDF real y extrayendo texto (REST API)..."
$tempDir = $env:TEMP
if (-not $tempDir) { $tempDir = (Get-Location).Path }
$pdfPath = Join-Path $tempDir "test_semana4.pdf"
Ensure-SamplePdf $pdfPath

# Windows PowerShell 5.1 no soporta -Form en Invoke-RestMethod.
$json = curl.exe -s -X POST -F "file=@$pdfPath" "$restApi/api/v1/pdf/extract"
$response = $json | ConvertFrom-Json
$text = [string]$response.text
Write-Host "Texto extraído (primeros 120 chars): $($text.Substring(0, [Math]::Min(120, $text.Length)))"

Write-Host "[3] Chat → MCP Tool (PDF) → Payment Service → webhook → Partner..."
$chatBody = @{
    message = "Procesa el PDF y ejecuta el flujo de pago"
    toolName = "pdf_to_partner_payment"
    toolArgs = @{
        text = $text
        partner_id = $partnerId
    }
} | ConvertTo-Json -Depth 6

$reply = Invoke-RestMethod -Uri "$aiOrchestrator/chat" -Method Post -Body $chatBody -ContentType "application/json"
Write-Host "Respuesta AI Orchestrator:"
Write-Host ($reply | ConvertTo-Json -Depth 8)

Write-Host "[4] Validación bidireccional: Partner PHP → Payment Service (/webhooks/partner)..."
$partnerTrigger = Invoke-RestMethod -Uri "$partnerPhp/partner/trigger" -Method Post
Write-Host ($partnerTrigger | ConvertTo-Json -Depth 6)

Write-Host "[5] Listando pagos (Payment Service)..."
$payments = Invoke-RestMethod -Uri "$paymentService/payments" -Method Get
Write-Host ($payments | ConvertTo-Json -Depth 6)

Write-Host "[OK] Test de integración Semana 4 COMPLETO."
