# Exports reales de n8n (Semana 3)

Esta carpeta contiene los **exports importables** de los workflows de Semana 3.

Si el docente exige que el export sea “generado desde la UI”, importa estos JSON en n8n y luego vuelve a **Download/Export** desde la UI; el JSON resultante también se guarda aquí.

## Requisito (docente)
Los workflows de Semana 3 deben ser exportables/importables desde n8n. Si no se adjuntan aquí, se deben dejar **pasos exactos** para exportar e importar.

## Archivos esperados
Archivos (recomendado):
- `payment_handler.json`
- `partner_handler.json`
- `scheduled_task_report.json`

## Cómo exportar (desde la UI)
1) Abre n8n: `http://localhost:5678`
2) Entra al Workflow.
3) Menú (⋯) → **Download** (o **Export** → Download).
4) Guarda el `.json` dentro de esta carpeta.

## Cómo importar
1) En n8n: Workflows → **Import from File**
2) Selecciona el `.json`.
3) Revisa los nodos Webhook/Cron y guarda.
