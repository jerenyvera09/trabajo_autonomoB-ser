# Semana 5 – Presentación y Entrega Final (Segundo Parcial)

Semana 5 se enfoca en el **refinamiento final**, **documentación completa** y **preparación de demo** para evidenciar los 4 pilares funcionando e integrados.

## 1) Checklist de entrega (según rúbrica)

### Pilar 1 – Auth Service
- Auth Service independiente con DB propia (PostgreSQL en `auth-db`).
- JWT access + refresh tokens.
- Validación local en servicios (sin consultar Auth en cada request).
- Seguridad: rate limiting login + revocación/blacklist.

Referencia:
- Auth Service: [sistema_de_informes/services/auth-service/README.md](../../services/auth-service/README.md)
- Semana 1: [sistema_de_informes/docs/segundo_parcial/semana_1.md](semana_1.md)

### Pilar 2 – Payment + Webhooks B2B
- Wrapper con Adapter Pattern (MockAdapter obligatorio).
- Registro de partners + secret compartido.
- HMAC-SHA256 para firmar y verificar webhooks.
- Flujo bidireccional (nuestro sistema ↔ partner PHP demo).

Referencia:
- Payment Service: [sistema_de_informes/services/payment-service/README.md](../../services/payment-service/README.md)
- Contrato/events: [sistema_de_informes/docs/partner/contrato_eventos.md](../partner/contrato_eventos.md)
- Semana 2–3: [sistema_de_informes/docs/segundo_parcial/semana_3.md](semana_3.md)

### Pilar 3 – MCP + IA
- AI Orchestrator con Strategy/Adapter para LLM.
- 5 Tools (2 consulta, 2 acción, 1 reporte).
- Entradas multimodales (mínimo 2 tipos) demostrables con scripts/guía.

Referencia:
- AI Orchestrator: [sistema_de_informes/services/ai-orchestrator/README.md](../../services/ai-orchestrator/README.md)
- Semana 3–4: [sistema_de_informes/docs/segundo_parcial/semana_4.md](semana_4.md)

### Pilar 4 – n8n Event Bus
Workflows operativos y exportables/importables:
- Payment Handler
- Partner Handler
- Scheduled Task
- MCP Input Handler (recomendado para demo)

Exports oficiales (compatibles con n8n `1.70.0`):
- [sistema_de_informes/docs/n8n/exports/payment_handler.json](../n8n/exports/payment_handler.json)
- [sistema_de_informes/docs/n8n/exports/partner_handler.json](../n8n/exports/partner_handler.json)
- [sistema_de_informes/docs/n8n/exports/scheduled_task_report.json](../n8n/exports/scheduled_task_report.json)
- [sistema_de_informes/docs/n8n/exports/mcp_input_handler.json](../n8n/exports/mcp_input_handler.json)

## 2) Guion de demo (10–15 minutos)

### 2.1 Levantar servicios
En la raíz del repo:

1) Levantar todo con Docker:
`docker compose up --build`

2) URLs para demo:
- REST API: `http://localhost:8000/docs`
- Auth Service: `http://localhost:8001/docs`
- Payment Service: `http://localhost:8002/docs`
- AI Orchestrator: `http://localhost:8003/docs`
- WebSocket health/notify: `http://localhost:8080/health`
- Partner PHP: `http://localhost:8088/health`
- MailHog UI (emails): `http://localhost:8025`
- n8n (este proyecto): `http://localhost:5679`

Nota: si en tu PC existe otro n8n en `5678`, este proyecto usa `5679` para evitar conflicto.

### 2.2 Importar/activar workflows en n8n (Pilar 4)
En n8n (`http://localhost:5679`):
1) Workflows → Import from File → importa los 4 JSON de `docs/n8n/exports/`.
2) Abre cada workflow y ponlo en **Activo** (toggle).

### 2.3 Flujo end-to-end recomendado

Opción A (rápida, para Pilar 4 + B2B + email + WS):
1) Disparar Payment Handler (n8n) con un payload de prueba.
2) Verificar:
	 - Email en MailHog (`http://localhost:8025`)
	 - Partner recibió webhook (respuesta OK)

Opción B (IA + MCP + tools):
1) Enviar mensaje a MCP Input Handler (`/webhook/mcp-input`) o directo a AI Orchestrator `/chat`.
2) Ejecutar tool de acción (ej. `create_payment`) y mostrar respuesta.

## 3) Script de demo (Windows)

Para una demo repetible en Windows (PowerShell), usa:
- [sistema_de_informes/scripts/semana5_demo.ps1](../../scripts/semana5_demo.ps1)

El script hace health checks, registra partner, dispara el webhook de n8n y consulta MailHog para evidenciar el correo.

## 4) Evidencias mínimas para la entrega
- Capturas de:
	- n8n con workflows activos
	- MailHog con email recibido
	- Swagger `/docs` de Auth/Payment/AI
	- Resultado de ejecución del script de demo