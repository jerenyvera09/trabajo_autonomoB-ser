# Exports reales de n8n (Pilar 4 - Semana 4)

Esta carpeta contiene los **exports importables** de los workflows del **Pilar 4 (n8n Event Bus)**.

Si el docente exige que el export sea “generado desde la UI”, importa estos JSON en n8n y luego vuelve a **Download/Export** desde la UI; el JSON resultante también se guarda aquí.

## Requisito (docente)
Los workflows del Pilar 4 deben ser **operativos** y **exportables/importables** desde n8n.

## Archivos esperados
Archivos (recomendado):
- `payment_handler.json`
- `partner_handler.json`
- `scheduled_task_report.json`
- `mcp_input_handler.json` (MCP Input Handler → AI Orchestrator)

## Qué cubre la rúbrica (Pilar 4)
- **Payment Handler**: webhook de entrada → **verificación HMAC** → validación payload → crear pago → activar acción interna + notificar WS → enviar email → disparar webhook al partner.
- **Partner Handler**: webhook de partner → verificación HMAC → procesar evento (acción interna) → ACK.
- **Scheduled Task**: cron → genera reporte → email del reporte.
- **MCP Input Handler** (opcional según rúbrica / recomendado para demo): webhook de entrada → normaliza mensaje → llama a AI Orchestrator (/chat).

## Cómo exportar (desde la UI)
1) Abre n8n: `http://localhost:5679`
2) Entra al Workflow.
3) Menú (⋯) → **Download** (o **Export** → Download).
4) Guarda el `.json` dentro de esta carpeta.

## Cómo importar
1) En n8n: Workflows → **Import from File**
2) Selecciona el `.json`.
3) Revisa los nodos Webhook/Cron y guarda.
