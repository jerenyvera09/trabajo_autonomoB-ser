# Segundo Parcial — Semana 2 (Cierre 100%)

**Fecha:** 29 de diciembre de 2025  
**Regla de oro:** este documento cubre **SOLO Semana 2**.

---

## A) Objetivo de Semana 2 (qué se construyó)

Semana 2 deja listo, funcional y demostrable localmente:

1) **Payment Service** (FastAPI) como microservicio independiente con **Adapter Pattern**.
   - Provider obligatorio: **MockAdapter** (sin integraciones externas).
   - Almacenamiento **en memoria** (sin DB).
   - Endpoints de checkout, consulta de pago y recepción de webhooks.

2) **Registro de partners (B2B)**.
   - Endpoint para registrar partners (nombre, webhook URL, eventos) y generar un **secret compartido**.

3) **Seguridad HMAC-SHA256**.
   - **Requisito literal de esta Semana 2:** **TODOS los webhooks requieren HMAC-SHA256** usando el **body raw completo**.

4) **AI Orchestrator (base)** (FastAPI).
   - **Strategy Pattern** para LLMs.
   - `MockLLM` (respuestas fijas, sin IA real).
   - Endpoint `POST /chat`.
   - 2 tools simples invocables: `info` y `action`.

5) **Dockerfiles + docker-compose.yml**.
   - `payment-service` en `8002`.
   - `ai-orchestrator` en `8003`.

---

## B) Estructura relevante del repo (rutas exactas)

- Microservicios:
  - `sistema_de_informes/services/payment-service`
  - `sistema_de_informes/services/ai-orchestrator`

- Infra:
  - `docker-compose.yml`

- Variables de entorno:
  - `.env.example` (raíz)
  - `sistema_de_informes/services/payment-service/.env.example`
  - `sistema_de_informes/services/ai-orchestrator/.env.example`

---

## C) Payment Service (Semana 2)

**URL local:** `http://localhost:8002`

### C.1 Adapter Pattern: PaymentProvider + MockAdapter

**Qué se cumple:**

- Interfaz `PaymentProvider` (contrato mínimo):
  - `create_payment(data)`
  - `get_payment_status(payment_id)`

- `MockAdapter` (obligatorio):
  - Genera IDs únicos (`pay_<hex>`).
  - Simula pago exitoso o fallido.
  - Cambia el estado del pago.
  - NO depende de servicios externos.

- `StripeAdapter`:
  - Existe solo como **placeholder**.
  - **No está implementado** en Semana 2 (prohibido integrar Stripe real).

### C.2 Endpoints (Semana 2) + ejemplos `curl`

#### 1) Health — `GET /health`

```bash
curl -i http://localhost:8002/health
```

**Esperado (200):**
```json
{"status":"ok","service":"payment-service"}
```

#### 2) Checkout — `POST /payments/checkout`

**Simular éxito:**

```bash
curl -i -X POST http://localhost:8002/payments/checkout \
  -H "Content-Type: application/json" \
  -d "{\"amount\": 10, \"currency\": \"USD\", \"simulate\": \"success\"}"
```

**Esperado (201):** `status: succeeded`.

**Simular fallo:**

```bash
curl -i -X POST http://localhost:8002/payments/checkout \
  -H "Content-Type: application/json" \
  -d "{\"amount\": 10, \"currency\": \"USD\", \"simulate\": \"fail\"}"
```

**Esperado (201):** `status: failed`.

#### 3) Consultar pago — `GET /payments/{payment_id}`

```bash
curl -i http://localhost:8002/payments/pay_REEMPLAZA
```

**Esperado:** 200 si existe / 404 si no existe.

#### 4) Registro de partners — `POST /partners/register`

> Retorna `partnerId` y `secret` (HMAC).

```bash
curl -i -X POST http://localhost:8002/partners/register \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Partner Demo\",\"webhookUrl\":\"http://localhost:9999/webhook\",\"events\":[\"payment.success\",\"payment.failed\"]}"
```

**Esperado (201):** JSON con `partnerId` y `secret`.

#### 5) Webhooks — `POST /webhooks/{provider}`

##### Normalización (siempre)

Todo webhook se retorna normalizado:

```json
{
  "event": "payment.success",
  "paymentId": "pay_...",
  "provider": "mock",
  "timestamp": "..."
}
```

##### Requisito literal: HMAC en TODOS los webhooks

- Header firma (por defecto): `X-Signature`
- Para `provider=partner` también se exige: `X-Partner-Id`

Los nombres de headers se pueden cambiar por env:
- `HMAC_HEADER_SIGNATURE` (default `X-Signature`)
- `HMAC_HEADER_PARTNER_ID` (default `X-Partner-Id`)

**Reglas de verificación:**
- `POST /webhooks/partner`: firma con el **secret del partner** (obtenido en `/partners/register`).
- `POST /webhooks/mock` y `POST /webhooks/stripe`: firma con `PAYMENT_SERVICE_SECRET_FALLBACK`.

> Si falta la firma o es inválida, el servicio responde **401**.

---

### C.3 Guía HMAC-SHA256 (OBLIGATORIO)

**Entrada:** `secret` + `body raw` (bytes EXACTOS)  
**Salida:** `hexdigest` (hex)

#### Snippet Python (hexdigest)

```python
import hmac
import hashlib

secret = "PEGA_AQUI_EL_SECRET"
body = b'{"type":"payment.success","paymentId":"pay_123"}'

sig = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
print(sig)
```

> Importante: el HMAC depende del body EXACTO (espacios/orden cambian el hash).

#### Ejemplo 1 — `/webhooks/mock` (usa secret fallback)

1) Define `PAYMENT_SERVICE_SECRET_FALLBACK` (en `.env` o env del contenedor).
2) Calcula firma del body que enviarás.
3) Envía el webhook:

```bash
curl -i -X POST http://localhost:8002/webhooks/mock \
  -H "Content-Type: application/json" \
  -H "X-Signature: FIRMA_HEX_REEMPLAZA" \
  -d "{\"type\":\"payment.success\",\"paymentId\":\"pay_123\"}"
```

**Esperado (200):** retorna el JSON normalizado.

#### Ejemplo 1.1 — `/webhooks/stripe` (stub, usa secret fallback)

> NO hay integración real con Stripe en Semana 2. Este endpoint existe únicamente para demostrar
> que la ruta `/webhooks/{provider}` y la verificación HMAC aplican a cualquier provider.

```bash
curl -i -X POST http://localhost:8002/webhooks/stripe \
  -H "Content-Type: application/json" \
  -H "X-Signature: FIRMA_HEX_REEMPLAZA" \
  -d "{\"type\":\"payment.failed\",\"paymentId\":\"pay_123\"}"
```

**Esperado (200):** retorna el JSON normalizado.

#### Ejemplo 2 — `/webhooks/partner` (usa secret del partner)

1) Registra partner y obtén `partnerId` + `secret`.
2) Firma el body con ese `secret`.
3) Envía:

```bash
curl -i -X POST http://localhost:8002/webhooks/partner \
  -H "Content-Type: application/json" \
  -H "X-Partner-Id: partner_REEMPLAZA" \
  -H "X-Signature: FIRMA_HEX_REEMPLAZA" \
  -d "{\"eventName\":\"payment.success\",\"payment\":{\"id\":\"pay_123\"}}"
```

**Esperado:**
- 200 si firma válida
- 401 si firma inválida
- 400 si falta `X-Partner-Id`

---

## D) AI Orchestrator (Semana 2)

**URL local:** `http://localhost:8003`

### D.1 Strategy Pattern: LLMProvider + MockLLM

- Interfaz `LLMProvider`: `generate(prompt) -> str`
- Implementación Semana 2: `MockLLM` (respuestas fijas)

**Aclaración explícita:** NO IA real, NO embeddings, NO OCR, NO multimodalidad.

### D.2 Endpoints + ejemplos `curl`

#### 1) Health — `GET /health`

```bash
curl -i http://localhost:8003/health
```

#### 2) Chat — `POST /chat`

**Chat simple:**

```bash
curl -i -X POST http://localhost:8003/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Hola\"}"
```

### D.3 Tools (Semana 2)

Tools disponibles (solo 2):
- `info` (consulta)
- `action` (acción simulada)

Se invocan con:
- `toolName` (string)
- `toolArgs` (objeto)

**Ejemplo tool `info`:**

```bash
curl -i -X POST http://localhost:8003/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Info\",\"toolName\":\"info\",\"toolArgs\":{}}"
```

**Ejemplo tool `action`:**

```bash
curl -i -X POST http://localhost:8003/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Acción\",\"toolName\":\"action\",\"toolArgs\":{\"action\":\"ping\",\"target\":\"payment-service\"}}"
```

---

## E) Cómo ejecutar (Docker y sin Docker)

### E.1 Docker (pasos exactos)

1) Copiar `.env.example` a `.env` (raíz):

CMD:
```bat
copy .env.example .env
```

2) Validar configuración:
```bash
docker compose config
```

3) (Opcional) Build explícito:
```bash
docker compose build payment-service ai-orchestrator
```

4) Levantar:
```bash
docker compose up --build
```

**Puertos esperados:**
- `8001` auth-service
- `8002` payment-service
- `8003` ai-orchestrator
- `5433` auth-db
- `5678` n8n

**Si aparece:** `dockerDesktopLinuxEngine ... cannot find the file specified`
- Significa que Docker Desktop/Engine está apagado.
- Solución: abrir Docker Desktop, esperar “Running”, y reintentar `docker compose up --build`.

### E.2 Sin Docker (smoke test)

Payment Service:
```bat
cd sistema_de_informes\services\payment-service
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\uvicorn main:app --reload --port 8002
```

AI Orchestrator:
```bat
cd sistema_de_informes\services\ai-orchestrator
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\uvicorn main:app --reload --port 8003
```

---

## F) Checklist final de verificación (Semana 2)

### F.1 Comandos de validación

- Validar compose:
```bash
docker compose config
```

- Compilar todo el Python:
```bash
python -m compileall
```

### F.2 Verificación mínima (requests)

1) Payment health:
```bash
curl -i http://localhost:8002/health
```

2) Checkout:
```bash
curl -i -X POST http://localhost:8002/payments/checkout -H "Content-Type: application/json" -d "{\"amount\":10,\"currency\":\"USD\",\"simulate\":\"success\"}"
```

3) Webhook mock SIN firma (debe fallar):
```bash
curl -i -X POST http://localhost:8002/webhooks/mock -H "Content-Type: application/json" -d "{\"type\":\"payment.success\",\"paymentId\":\"pay_123\"}"
```
**Esperado:** `401`.

4) Webhook mock CON firma (debe pasar):
- Calcula firma con `PAYMENT_SERVICE_SECRET_FALLBACK` + body raw.
- Envía con `X-Signature`.

5) AI health:
```bash
curl -i http://localhost:8003/health
```

6) Chat:
```bash
curl -i -X POST http://localhost:8003/chat -H "Content-Type: application/json" -d "{\"message\":\"Hola\"}"
```

---

## Lo NO implementado en Semana 2 (por diseño)

- Stripe/MercadoPago reales
- Workflows de n8n
- Webhooks bidireccionales funcionando
- Frontend
- IA real / OCR / embeddings / multimodalidad
