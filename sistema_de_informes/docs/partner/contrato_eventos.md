# Contrato de eventos B2B (Partner) – Semana 3

Este documento define el contrato mínimo de eventos y seguridad (HMAC) para interoperabilidad B2B.

## Partner utilizado en Semana 3

Para cumplir el requisito de bidireccionalidad cuando no se consigue un grupo externo (según indicación del docente), se usa un **partner de demostración** implementado en PHP en `backend_php/`.

Este partner representa un sistema B2B externo y permite evidenciar:
- Registro de partner
- Firma/verificación HMAC
- Flujo bidireccional (nuestro sistema ↔ partner)

## Eventos soportados (Semana 3)

- `payment.success`
- `booking.confirmed` (opcional)
- `tour.purchased`
- `service.activated` (opcional)

## Formato de payload (común)

Todos los webhooks usan este formato JSON:

```json
{
  "event": "tour.purchased",
  "data": { "...": "..." },
  "timestamp": "2026-01-15T00:00:00Z",
  "source": "partner-php"
}
```

## Seguridad: HMAC-SHA256

- Header requerido: `X-Signature: <hex>`
- La firma se calcula como: `hex(hmac_sha256(raw_body, shared_secret))`

Cuando el receptor necesita identificar al partner (ej. `payment-service`), además se envía:

- `X-Partner-Id: <partnerId>`

## Nota de alcance

- Alcance Semana 3: contrato + pruebas bidireccionales (partner simulado) + verificación HMAC.
- No se incluye trabajo de Semana 4 (UI de chat/pagos, multimodal real, integración completa end-to-end).
