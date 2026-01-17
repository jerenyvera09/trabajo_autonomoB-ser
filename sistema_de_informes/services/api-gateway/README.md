# API Gateway (Segundo Parcial)

Este servicio expone un **punto de entrada único** para cumplir el requisito de integración entre microservicios:

- REST API (P1): `/api/v1/*`, `/docs`, `/openapi.json`
- Auth Service (Pilar 1): `/auth/*`
- Payment Service (Pilar 2): `/payments/*`, `/partners/*`, `/webhooks/*`
- AI Orchestrator (Pilar 3): `/ai/*` (proxy hacia `/` y `/chat` del servicio real)
- GraphQL (P1): `/graphql` (proxy con rewrite a `/` en el servidor Apollo)
- WebSocket (P1): `/ws` (proxy WebSocket hacia el servicio `ws`)

## Endpoints

- `GET /health` → `{"status":"ok","service":"api-gateway"}`
- `/{path:path}` → proxy HTTP hacia el backend correspondiente
- `WS /ws` → proxy WebSocket (preserva query: `room`, `token`, etc.)

## Variables de entorno

- `REST_API_URL` (default `http://rest-api:8000`)
- `AUTH_SERVICE_URL` (default `http://auth-service:8001`)
- `PAYMENT_SERVICE_URL` (default `http://payment-service:8002`)
- `AI_ORCHESTRATOR_URL` (default `http://ai-orchestrator:8003`)
- `GRAPHQL_URL` (default `http://graphql:4000`)
- `WS_URL` (default `ws://ws:8080/ws`)

## Docker

Se levanta desde el `docker-compose.yml` de la raíz.

## Nota

La lógica de ruteo y rewrite está en `main.py`.
