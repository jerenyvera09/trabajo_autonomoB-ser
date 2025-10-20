# 📋 Documentación de Integración - Semana 5

## Arquitectura del Sistema

El sistema está compuesto por **cuatro componentes principales** que se comunican entre sí:

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                         │
│                   http://localhost:3000                      │
└─────────────┬──────────────┬──────────────┬─────────────────┘
              │              │              │
              │ HTTP         │ HTTP         │ WebSocket
              │ GET /api/v1  │ POST /graphql│ ws://...
              ▼              ▼              ▼
   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
   │  REST API    │ │   GraphQL    │ │  WebSocket   │
   │  (FastAPI)   │ │   (Apollo)   │ │   (Go)       │
   │  :8000       │ │   :4000      │ │   :8080      │
   └──────────────┘ └──────┬───────┘ └──────────────┘
          │                │
          │                │ fetch()
          │                │ http://localhost:8000
          │                ▼
          │         ┌──────────────┐
          └────────►│   SQLite DB  │
                    │              │
                    └──────────────┘
```

---

## Flujos de Integración

### 1️⃣ Consulta de Reportes vía REST

```
Usuario → Frontend → REST API → SQLite → Respuesta JSON
```

**Endpoint**: `GET http://localhost:8000/api/v1/reports`

**Respuesta**:

```json
[
  {
    "id": "1",
    "title": "Fuga de agua",
    "description": "...",
    "status": "Abierto",
    "priority": "Media"
  }
]
```

---

### 2️⃣ Consulta de Reportes vía GraphQL

```
Usuario → Frontend → GraphQL → REST API → SQLite → Respuesta
```

**Query**:

```graphql
query {
  reports {
    id
    title
    description
    status
    priority
  }
}
```

El resolver de GraphQL internamente hace:

```typescript
fetch("http://localhost:8000/api/v1/reports");
```

---

### 3️⃣ Notificaciones en Tiempo Real (WebSocket)

```
Evento → WebSocket Server → Broadcast a todos los clientes conectados
```

**Mensaje enviado**:

```json
{
  "event": "new_report",
  "message": "Se ha creado un nuevo reporte"
}
```

**Comportamiento del Frontend**:

1. Recibe el mensaje WebSocket
2. Muestra banner de notificación
3. Recarga automáticamente los reportes desde REST y GraphQL
4. Oculta el banner después de 5 segundos

---

## Características de cada Servicio

### 🐍 REST API (Python/FastAPI)

- **Puerto**: 8000
- **Base de datos**: SQLite
- **CORS**: Habilitado para todos los orígenes
- **Endpoints principales**:
  - `GET /health` - Health check
  - `GET /api/v1/reports` - Listado simplificado
  - `GET /reportes` - CRUD completo con autenticación
  - `POST /auth/login` - Autenticación JWT

### 🧠 GraphQL (TypeScript/Apollo)

- **Puerto**: 4000
- **Playground**: http://localhost:4000/graphql
- **Queries disponibles**:
  - `reports` - Consume REST API
  - `reportes` - Mock local (Semana 4)
  - `health` - Health check
- **Mutations**: Crear reportes (mock)

### ⚙️ WebSocket (Go/Gorilla)

- **Puerto**: 8080
- **Protocolo**: WebSocket (ws://)
- **Endpoints**:
  - `GET /` - Health check
  - `WS /ws` - Conexión WebSocket
  - `POST /notify` - Simular notificación
- **Características**:
  - Broadcast a todos los clientes
  - Reconexión automática
  - Keepalive con pings

### 🖥️ Frontend (React/TypeScript)

- **Puerto**: 3000
- **Framework**: Vite + React 18
- **Características**:
  - Consumo de REST API
  - Consumo de GraphQL
  - Conexión WebSocket persistente
  - Notificaciones en tiempo real
  - Interfaz responsiva

---

## Comandos de Ejecución

### Iniciar todos los servicios

**Terminal 1 - REST API:**

```bash
cd sistema_de_informes/services/rest-api
uvicorn main:app --reload --port 8000
```

**Terminal 2 - GraphQL:**

```bash
cd sistema_de_informes/services/graphql
npm install
npm run dev
```

**Terminal 3 - WebSocket:**

```bash
cd sistema_de_informes/services/ws
go run main.go
```

**Terminal 4 - Frontend:**

```bash
cd sistema_de_informes/apps/frontend
npm install
npm run dev
```

---

## Pruebas de Integración

### 1. Verificar que todos los servicios estén activos

```bash
# REST API
curl http://localhost:8000/health

# GraphQL (en navegador)
http://localhost:4000/graphql

# WebSocket
curl http://localhost:8080/

# Frontend (en navegador)
http://localhost:3000
```

### 2. Probar flujo REST → Frontend

1. Abre el frontend en http://localhost:3000
2. Verifica que aparezcan reportes en la sección "REST API"
3. Click en "🔄 Actualizar REST"
4. Los datos deben recargarse

### 3. Probar flujo GraphQL → REST → Frontend

1. En el frontend, verifica la sección "GraphQL"
2. Click en "🔄 Actualizar GraphQL"
3. GraphQL consulta internamente al REST
4. Los datos se muestran en el frontend

### 4. Probar WebSocket → Frontend

**Opción A - Simular evento manualmente:**

```bash
curl -X POST http://localhost:8080/notify \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"¡Nuevo reporte creado desde terminal!\"}"
```

**Opción B - Conectarse y enviar mensaje:**

1. Usa PieSocket o wscat: `wscat -c ws://localhost:8080/ws`
2. Envía: `new_report`
3. Observa el banner en el frontend

**Resultado esperado:**

- ✅ Banner verde aparece en la esquina superior derecha
- ✅ Reportes se recargan automáticamente
- ✅ Banner desaparece después de 5 segundos

---

## Tecnologías Utilizadas

| Componente    | Tecnología        | Versión | Puerto |
| ------------- | ----------------- | ------- | ------ |
| REST API      | Python/FastAPI    | 0.115.5 | 8000   |
| GraphQL       | TypeScript/Apollo | 4.11.2  | 4000   |
| WebSocket     | Go/Gorilla        | 1.23    | 8080   |
| Frontend      | React/Vite        | 18.2    | 3000   |
| Base de Datos | SQLite            | 3.x     | -      |

---

## Estructura de Carpetas

```
sistema_de_informes/
├── services/
│   ├── rest-api/         # Python/FastAPI
│   │   ├── main.py
│   │   ├── entities/
│   │   ├── routers/
│   │   └── schemas/
│   ├── graphql/          # TypeScript/Apollo
│   │   ├── src/
│   │   │   ├── index.ts
│   │   │   ├── schema.ts
│   │   │   └── resolvers/
│   │   └── package.json
│   └── ws/               # Go/Gorilla
│       ├── main.go
│       └── go.mod
├── apps/
│   └── frontend/         # React/Vite
│       ├── src/
│       │   ├── App.tsx
│       │   └── index.css
│       └── package.json
└── docs/
    └── integracion.md    # Este archivo
```

---

## Troubleshooting

### Frontend no carga datos

- ✅ Verifica que REST API esté en puerto 8000
- ✅ Verifica que GraphQL esté en puerto 4000
- ✅ Revisa la consola del navegador (F12)

### WebSocket no conecta

- ✅ Verifica que el servidor Go esté corriendo
- ✅ Revisa que no haya firewalls bloqueando el puerto 8080
- ✅ El frontend intentará reconectar automáticamente

### CORS errors

- ✅ Todos los servicios tienen CORS habilitado
- ✅ Verifica que las URLs en `.env` sean correctas

---

✅ **Documentación completa - Semana 5**
