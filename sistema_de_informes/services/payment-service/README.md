# Payment Service (Semana 2–3)

Microservicio FastAPI que abstrae pasarelas de pago mediante **Adapter Pattern** y gestiona interoperabilidad B2B mediante **webhooks firmados con HMAC-SHA256**.

## Endpoints

### Salud
- `GET /health` → `{"status":"ok","service":"payment-service"}`

### Pagos (MockAdapter)
- `POST /payments/checkout` → crea un pago (mock)
- `GET /payments/{payment_id}` → consulta estado

### Partners (B2B)
- `POST /partners/register` → registra partner y genera `partnerId` + `secret`
- `POST /partners/{partner_id}/send-test` → (Semana 3) envía un webhook firmado al partner registrado (dirección: nuestro sistema → partner)

### Recepción de webhooks
- `POST /webhooks/{provider}`
  - `provider=partner`: requiere `X-Partner-Id` + `X-Signature` (HMAC con el `secret` del partner)
  - `provider=mock` u otros: usa `PAYMENT_SERVICE_SECRET_FALLBACK`

## Headers HMAC

- `X-Signature: <hex>` donde `<hex>` = `hmac_sha256(raw_body, secret)`
- Para `provider=partner` también:
  - `X-Partner-Id: <partnerId>`

## Prueba bidireccional con partner PHP (Semana 3)

La guía completa está en:
- [sistema_de_informes/docs/segundo_parcial/semana_3.md](../../docs/segundo_parcial/semana_3.md)

Resumen:
1) Levanta `partner-php` con compose.
2) Registra partner (`/partners/register`) y toma `partnerId` + `secret`.
3) Prueba:
   - nuestro sistema → partner: `POST /partners/{partnerId}/send-test`
  - partner → nuestro sistema: `POST http://localhost:8088/partner/trigger`
