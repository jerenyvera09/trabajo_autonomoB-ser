# AI Orchestrator (Semana 3)

Microservicio FastAPI que orquesta llamadas a un LLM mediante un **Adapter/Strategy** y expone un endpoint `/chat` con soporte de **MCP Tools**.

## Endpoints

- `GET /health` → `{"status":"ok","service":"ai-orchestrator"}`
- `POST /chat`

## LLM Provider (Strategy)

Se selecciona con `LLM_PROVIDER`:
- `mock` (default): responde texto simulado
- `real`: stub con comentarios STOP (no se integra en Semana 3)

## MCP Tools (Semana 3)

Tools registradas (mínimo 5):
- Consulta: `info`, `query_user`, `query_payment`
- Acción: `create_payment`, `activate_service`
- Reporte: `report`

Uso típico:
- Enviar `message` y opcionalmente `toolName` + `toolArgs`.

La descripción detallada y alcance de Semana 3 está en:
- [sistema_de_informes/docs/segundo_parcial/semana_3.md](../../docs/segundo_parcial/semana_3.md)
