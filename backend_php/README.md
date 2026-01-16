# Partner simulado (PHP)

Este servicio implementa un **partner simulado** en PHP, pensado para probar webhooks **bidireccionales** con **firma HMAC-SHA256**.

- Recibe webhooks desde tu sistema en `POST /partner/webhook` y **verifica** `X-Signature`.
- Dispara webhooks hacia tu sistema en `POST /partner/trigger` y **firma** `X-Signature`.
- Salud en `GET /health`.

## Puertos

Este contenedor usa Apache en el puerto **80** dentro del contenedor.

Recomendación (y snippet incluido): publicar en host como:

- `http://localhost:8088`  → contenedor `:80`

## Variables de entorno

- `PARTNER_SHARED_SECRET` (requerida): secreto compartido para HMAC.
- `TARGET_URL` (requerida para `/partner/trigger`): URL destino donde el partner enviará el webhook.
- `OUR_PARTNER_HANDLER_URL` (opcional): compatibilidad (si `TARGET_URL` no está definida).
- `PARTNER_ID` (opcional): si el receptor exige identificar al partner (ej. `payment-service`), se enviará `X-Partner-Id: <PARTNER_ID>`.

## Levantar con Docker Compose (sin tocar tu compose principal)

Hay un archivo listo para usar: [backend_php/docker-compose.partner-php.yml](backend_php/docker-compose.partner-php.yml)

Ejecuta desde la raíz del repo:

```bash
docker compose -f docker-compose.yml -f backend_php/docker-compose.partner-php.yml up --build partner-php
```

Esto conecta `partner-php` a la misma red Docker del proyecto: `informes_net` (ya definida en tu `docker-compose.yml`).

## Levantar con Docker (sin compose)

Desde la raíz del repo:

```bash
docker build -t partner-php ./backend_php

docker run --rm -p 8088:80 \
  -e PARTNER_SHARED_SECRET="dev-partner-secret-change-me" \
  -e TARGET_URL="http://localhost:8002/webhooks/partner" \
  partner-php
```

Nota: en modo `docker run` estás fuera de la red `informes_net`; para enviar a servicios del compose por nombre (ej. `http://rest-api:8000/...`) conviene usar el compose combinado.

---

## Probar `GET /health`

```bash
curl -i http://localhost:8088/health
```

Esperado:

```json
{"status":"ok","service":"partner-php"}
```

## Probar `POST /partner/webhook` (tu sistema -> partner)

### 1) Armar un body JSON (IMPORTANTE: la firma se calcula sobre el body exacto)

En Windows (PowerShell):

```powershell
$body = '{"event":"payment.confirmed","data":{"payment_id":"p_123"},"timestamp":"2026-01-15T00:00:00Z","source":"our-system"}'
```

### 2) Calcular firma HMAC-SHA256 en hex

Con `openssl` (PowerShell):

```powershell
$secret = "dev-partner-secret-change-me"
$signature = $body | openssl dgst -sha256 -hmac $secret | % { $_.ToString().Split(' ')[-1] }
$signature
```

### 3) Enviar el webhook al partner

```powershell
curl -i -X POST http://localhost:8088/partner/webhook `
  -H "Content-Type: application/json" `
  -H "X-Signature: $signature" `
  --data $body
```

Respuesta esperada (200):

```json
{"status":"ack","received_event":"payment.confirmed"}
```

Si la firma no coincide: **401**.

## Probar bidireccionalidad `POST /partner/trigger` (partner -> tu sistema)

Este endpoint genera un evento simulado `tour.purchased` y lo envía a `TARGET_URL` con firma HMAC.

### Con compose (recomendado)

1) Asegúrate de tener el servicio destino levantado (en Semana 3 se usa `payment-service`).
2) Configura `TARGET_URL` apuntando al handler dentro de la red Docker.

Ejemplo (recomendado para Semana 3, usando el Payment Service como receptor):

1) Registra este partner en el Payment Service para obtener `partnerId` y `secret`:

```bash
curl -i -X POST http://localhost:8002/partners/register \
  -H "Content-Type: application/json" \
  --data '{"name":"partner-php","webhookUrl":"http://partner-php/partner/webhook","events":["tour.purchased"]}'
```

2) Toma el `secret` del response y configúralo en `PARTNER_SHARED_SECRET` del contenedor `partner-php`.

3) Toma el `partnerId` del response y configúralo en `PARTNER_ID` del contenedor `partner-php`.

4) Configura el destino para el trigger:

- `TARGET_URL=http://payment-service:8002/webhooks/partner`

Luego dispara:

```bash
curl -i -X POST http://localhost:8088/partner/trigger
```

Respuesta esperada (200) incluye:
- `downstream.status_code`
- `downstream.response_body`

---

## Snippet para copiar al compose principal (opcional)

Si prefieres copiar/pegar en el `docker-compose.yml` de la raíz (sin cambiar servicios existentes), la sección mínima es:

```yml
  partner-php:
    build:
      context: ./backend_php
    environment:
      PARTNER_SHARED_SECRET: ${PARTNER_SHARED_SECRET:-dev-partner-secret-change-me}
      PARTNER_ID: ${PARTNER_ID:-}
      TARGET_URL: ${TARGET_URL:-http://payment-service:8002/webhooks/partner}
    ports:
      - "8088:80"
    networks:
      - informes_net
```

(La red `informes_net` ya existe en tu compose actual.)
