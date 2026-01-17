# Semana 3 – Avances Técnicos

## Pilar 3: AI Orchestrator (MCP)

- Se implementó el microservicio **AI Orchestrator** con FastAPI.
- Se aplicó el patrón Strategy para el **LLM Adapter**:
  - `MockLLMAdapter`: funcional, responde con mensajes simulados.
  - `RealLLMAdapter`: preparado como stub, pendiente de integración real (comentario STOP).
- Se implementaron **6 tools MCP** (cumple mínimo 5). En Semana 3 se integraron **3** con el `payment-service`:
  - **Consulta:**
    - `info`: información del orquestador (local).
    - `query_user`: consulta real si se provee `token` (valida contra `auth-service` en `GET /auth/validate`).
    - `query_payment`: consulta real al `payment-service` (`GET /payments/{id}`).
  - **Acción:**
    - `create_payment`: acción real al `payment-service` (`POST /payments/checkout`).
    - `activate_service`: acción real que dispara un webhook firmado al partner vía `payment-service` (`POST /partners/{partnerId}/send-test`).
  - **Reporte:**
    - `report`: reporte real consultando el `payment-service` (`GET /payments`).
- Toda llamada a IA pasa por el Adapter.
- Las tools integradas usan `PAYMENT_SERVICE_URL` (por defecto `http://payment-service:8002`).
- Se agregaron logs claros de inicio y ejecución en el orquestador.

## Pilar 4: n8n (Workflows)

- Se definió el workflow **Payment Handler** usando MockAdapter (no requiere integración real).
- Se definió la estructura del workflow **Partner Handler** para recibir eventos externos (incluye guía para validar HMAC).
- Se creó un **Scheduled Task** (cron job) funcional que simula el envío de un reporte diario.
- Para cumplir el requisito del docente (“export real”), se deja:
  - **Plantillas** (NO export real) en `sistema_de_informes/docs/n8n/templates/`
  - **Exports reales** (generados desde la UI de n8n) en `sistema_de_informes/docs/n8n/exports/`

### Cómo crearlos en n8n + exportarlos (Semana 3)

1) Abre n8n: `http://localhost:5679`.
2) Crea 3 workflows:
  - **Payment Handler**
  - **Partner Handler**
  - **Scheduled Task**
3) Usa como referencia las plantillas en `sistema_de_informes/docs/n8n/templates/`.
4) Exporta cada workflow desde la UI:
  - Abre el workflow
  - Menú (⋯) → **Download** (o **Export** → Download)
  - Guarda el JSON en `sistema_de_informes/docs/n8n/exports/`
5) Importar (si hace falta): Workflows → **Import from File**.

## Validaciones y Restricciones

- Todos los servicios arrancan correctamente y muestran logs de arranque/ejecución.
- Para cumplir la interoperabilidad B2B en Semana 3 sin depender de un grupo externo, se agregó una **pila 2** con un **partner simulado en PHP** (carpeta `backend_php/` en la raíz del repo).
- La bidireccionalidad y la firma HMAC se demuestran contra el Payment Service.
- El alcance se mantiene en Semana 3: no se implementa UI de chat/pagos ni features extra de Semana 4.

---

**Nota:** Para pruebas, revisar los endpoints del AI Orchestrator. Las tools MCP pueden invocarse vía `/chat` especificando el nombre de la tool y argumentos mock.

Ejemplos (AI Orchestrator en `http://localhost:8003`):

```bash
curl -s -X POST http://localhost:8003/chat -H "Content-Type: application/json" \
  -d '{"message":"crear pago","toolName":"create_payment","toolArgs":{"amount":10,"currency":"USD"}}'
```

```bash
curl -s -X POST http://localhost:8003/chat -H "Content-Type: application/json" \
  -d '{"message":"reporte","toolName":"report","toolArgs":{}}'
```

---

## Pruebas B2B con Partner simulado (PHP) – Semana 3

### 1) Levantar el partner PHP (pila 2) en la misma red Docker

Desde la raíz (ya está en el `docker-compose.yml` principal y en la red `informes_net`):

```bash
docker compose up -d --build partner-php payment-service
```

Salud:

```bash
curl -i http://localhost:8088/health
```

### 2) Registrar el partner en Payment Service (genera `partnerId` + `secret`)

```bash
curl -i -X POST http://localhost:8002/partners/register \
  -H "Content-Type: application/json" \
  --data '{"name":"partner-php","webhookUrl":"http://partner-php/partner/webhook","events":["tour.purchased","payment.success"]}'
```

- Guarda el `partnerId` y el `secret`.
- Configura esos valores en el contenedor `partner-php` (variables `PARTNER_ID` y `PARTNER_SHARED_SECRET`).

### 3) Probar dirección A (nuestro sistema -> partner)

Se agregó un endpoint de prueba en el Payment Service para enviar un webhook firmado al partner registrado:

```bash
curl -i -X POST http://localhost:8002/partners/<partnerId>/send-test
```

Resultado esperado:
- El Payment Service responde `200` con `downstream.status_code`.
- El partner PHP responde ACK `{"status":"ack",...}` si la firma coincide.

### 4) Probar dirección B (partner -> nuestro sistema)

El partner PHP genera `tour.purchased` y lo envía a:

- `http://payment-service:8002/webhooks/partner`

Incluye:
- `X-Signature` (HMAC-SHA256 del body)
- `X-Partner-Id` (desde `PARTNER_ID`)

Ejecución:

```bash
curl -i -X POST http://localhost:8088/partner/trigger
```

Resultado esperado:
- `partner-php` responde 200 con `downstream.status_code` (debería ser 200 si la firma es válida).

---

## Script de pruebas automático (PowerShell) – Semana 3

Para evitar errores en demo, se incluye un script que:
- Levanta `payment-service` + `partner-php`
- Registra partner
- Reconfigura `partner-php` con `partnerId/secret`
- Ejecuta pruebas bidireccionales + prueba negativa (401)

Archivo:
- `sistema_de_informes/scripts/semana3_partner_tests.ps1`

También se incluye un script de demo más corto (solo 200/200) si prefieres algo directo:
- `sistema_de_informes/scripts/semana3_partner_demo.ps1`

Ejecución desde la raíz (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File sistema_de_informes/scripts/semana3_partner_tests.ps1
```

```powershell
powershell -ExecutionPolicy Bypass -File sistema_de_informes/scripts/semana3_partner_demo.ps1
```
