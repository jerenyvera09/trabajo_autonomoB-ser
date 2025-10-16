# Pruebas de Integración — Semana 6 (Commit 4)

Este documento guía pruebas punta-a-punta para REST, GraphQL, WebSocket y Frontend.

## 1) REST API

1. Health
   - GET http://localhost:8000/health → `{ "status":"ok" }`

2. Registro y Login
   - POST /auth/register (body: nombre, email, password)
   - POST /auth/login → obtiene `access_token`

3. CRUD mínimo de Reporte (rutas protegidas: usa `Authorization: Bearer <token>`)
   - POST /reportes → crear
   - GET /reportes → listar
   - PUT /reportes/{id} → actualizar
   - DELETE /reportes/{id} → eliminar

4. Endpoint de integración
   - GET /api/v1/reports → lista simplificada para GraphQL/Frontend

5. Errores
   - Probar validación 422 (por ejemplo, título demasiado corto)
   - Probar 401 sin token

## 2) GraphQL (http://localhost:4000/graphql)

- `reports` (paginación/filtros)
- `report(id: ID!)`
- `reportsAnalytics` (KPIs)

Ejemplo:

```graphql
query {
  reports(limit: 5) {
    total
    items {
      id
      title
      status
    }
  }
  reportsAnalytics {
    total
    byStatus {
      clave
      valor
    }
  }
}
```

## 3) WebSocket (ws://localhost:8080/ws?room=reports)

- Conectarse con un cliente WS (wscat/DevTools).
- Enviar `new_report` desde un cliente y observar broadcast.
- Simular desde REST un `update_report` (al actualizar/eliminar reporte) o con curl:

```bash
curl -X POST http://localhost:8080/notify/reports \
  -H "Content-Type: application/json" \
  -d '{"event":"update_report","message":"Reporte actualizado"}'
```

## 4) Frontend (http://localhost:3000)

- Ver listas REST y GraphQL.
- Ver notificaciones en tiempo real al disparar `new_report` o `update_report`.
- Ver KPIs en la sección de estadísticas (GraphQL → reportsAnalytics).

## 5) Secuencia sugerida (todo junto)

1. Levantar REST (:8000), GraphQL (:4000), WS (:8080) y Frontend (:3000).
2. Registrar usuario y hacer login en REST; crear 2–3 reportes.
3. Abrir el frontend y verificar paneles REST/GraphQL.
4. Actualizar un reporte (REST) y observar notificación en frontend.
5. Consultar `reportsAnalytics` en GraphQL y ver los KPIs en el frontend.
