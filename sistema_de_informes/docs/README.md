# 📚 Documentación del Sistema de Reportes

Índice central de toda la documentación del proyecto. Aquí encontrarás arquitectura, diagramas, guías de integración y contratos de APIs.

---

## 🗂️ Estructura de documentación

```
docs/
├── README.md                     # Este archivo (índice)
├── arquitectura.png              # Diagrama de arquitectura del sistema
├── uml.png                       # Diagrama UML de entidades
├── arquitectura_integracion.txt  # Descripción textual de la arquitectura
└── integracion.md                # Guía de integración entre servicios
```

---

## 🏗️ Arquitectura del Sistema

### Diagrama de arquitectura

![Arquitectura del Sistema](./arquitectura.png)

**Componentes principales:**

1. **Frontend (React + TypeScript + Vite)** - Puerto 3000
   - Interfaz de usuario responsiva
   - Integración con los 3 servicios backend
   - Notificaciones en tiempo real vía WebSocket

2. **REST API (Python + FastAPI)** - Puerto 8000
   - CRUD de entidades (reportes, usuarios, categorías, etc.)
   - Autenticación con JWT
   - Notificaciones a WebSocket cuando se crean reportes
   - Documentación automática en `/docs`

3. **GraphQL Server (TypeScript + Apollo Server)** - Puerto 4000
   - Queries analíticas (11 queries compuestas)
   - Exportación a PDF con `reportAnalytics`
   - Consume datos del REST API vía DataSource
   - Playground en `/graphql`

4. **WebSocket Server (Go + Gorilla)** - Puerto 8080
   - Notificaciones en tiempo real por rooms
   - Sistema de ping/pong para keep-alive
   - Autenticación con tokens JWT
   - Endpoints de notificación REST

**Flujo de datos:**

```
Frontend → REST API → Base de datos (Supabase/PostgreSQL)
         ↓
         → GraphQL → REST API (DataSource)
         ↓
         → WebSocket (notificaciones en tiempo real)
```

**Tecnologías:**

- **Frontend:** React 18, TypeScript, Vite, Apollo Client
- **REST API:** Python 3.11, FastAPI, SQLAlchemy, Pydantic
- **GraphQL:** Node.js 18, Apollo Server 4, TypeScript
- **WebSocket:** Go 1.21, Gorilla WebSocket
- **Base de datos:** PostgreSQL (Supabase)
- **Auth:** JWT (JSON Web Tokens)

---

## 📐 Diagrama UML

![Diagrama UML](./uml.png)

**Entidades principales:**

1. **Usuario** (User)
   - id, name, email, password_hash, role_id, created_at

2. **Rol** (Role)
   - id, name, permissions

3. **Reporte** (Report)
   - id, title, description, status, priority, category_id, area_id, user_id, created_at, updated_at

4. **Categoría** (Category)
   - id, name, description

5. **Área** (Area)
   - id, name, responsable

6. **Estado** (State)
   - id, name, is_final

7. **Comentario** (Comment)
   - id, content, report_id, user_id, created_at

8. **Puntuación** (Rating)
   - id, value, report_id, user_id, created_at

9. **Etiqueta** (Tag)
   - id, name

10. **ArchivoAdjunto** (Attachment)
    - id, filename, url, report_id, created_at

**Relaciones:**

- Usuario → Reporte (1:N)
- Reporte → Comentarios (1:N)
- Reporte → Puntuaciones (1:N)
- Reporte → Archivos Adjuntos (1:N)
- Categoría → Reportes (1:N)
- Área → Reportes (1:N)

---

## 🔗 Guía de Integración

Ver archivo detallado: [`integracion.md`](./integracion.md)

**Resumen de integraciones:**

### REST ↔ Frontend

```typescript
// Ejemplo: Crear reporte desde Frontend
const response = await fetch("http://localhost:8000/api/v1/reports", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  },
  body: JSON.stringify({
    title: "Nuevo reporte",
    description: "Descripción del problema",
    category_id: 1,
    area_id: 2,
    priority: "Alta",
  }),
});
```

### GraphQL ↔ Frontend

```typescript
// Ejemplo: Consultar reportes desde Frontend
import { useQuery, gql } from "@apollo/client";

const GET_REPORTS = gql`
  query GetReports($limit: Int, $offset: Int) {
    reports(limit: $limit, offset: $offset) {
      items {
        id
        title
        status
        priority
      }
      total
    }
  }
`;

const { data, loading } = useQuery(GET_REPORTS, {
  variables: { limit: 10, offset: 0 },
});
```

### WebSocket ↔ Frontend

```typescript
// Ejemplo: Conectar y recibir notificaciones
const ws = new WebSocket("ws://localhost:8080/ws?room=reports");

ws.onmessage = (event) => {
  const notification = JSON.parse(event.data);
  console.log("Nueva notificación:", notification.message);
  // Actualizar UI con nueva notificación
};

ws.onopen = () => console.log("✅ Conectado a WebSocket");
ws.onerror = (err) => console.error("❌ Error WebSocket:", err);
```

### REST → WebSocket (notificaciones)

```python
# Ejemplo: Notificar desde REST API cuando se crea un reporte
import requests

def notify_new_report(report_id: int):
    requests.post(
        'http://localhost:8080/notify/reports',
        json={'message': f'Nuevo reporte creado: {report_id}'}
    )
```

---

## 📄 Contratos de APIs

### REST API Endpoints

**Autenticación:**

- `POST /api/v1/auth/login` - Login con email/password → JWT
- `POST /api/v1/auth/register` - Registrar nuevo usuario

**Reportes:**

- `GET /api/v1/reports` - Listar reportes (paginado)
- `GET /api/v1/reports/{id}` - Obtener reporte por ID
- `POST /api/v1/reports` - Crear nuevo reporte
- `PUT /api/v1/reports/{id}` - Actualizar reporte
- `DELETE /api/v1/reports/{id}` - Eliminar reporte

**Categorías, Áreas, Estados:**

- `GET /api/v1/categories` - Listar categorías
- `GET /api/v1/areas` - Listar áreas
- `GET /api/v1/states` - Listar estados

**Archivos:**

- `POST /api/v1/attachments` - Subir archivo adjunto
- `GET /api/v1/attachments/{id}` - Descargar archivo

**Documentación interactiva:** http://localhost:8000/docs

---

### GraphQL Queries

**Queries básicas:**

```graphql
# Listar reportes
query {
  reports(limit: 10, offset: 0) {
    items {
      id
      title
      status
    }
    total
  }
}

# Obtener un reporte
query {
  reporte(id: "1") {
    id
    title
    description
    comentarios {
      content
      author {
        name
      }
    }
  }
}
```

**Queries analíticas (11 queries):**

1. `statsReportes` - Estadísticas generales
2. `reportesPorArea(area: String!)` - Filtrar por área
3. `topAreas(limit: Int)` - Top áreas con más reportes
4. `reportesPorCategoria(categoria: String!)` - Filtrar por categoría
5. `promedioPuntuaciones` - Promedio de ratings
6. `etiquetasMasUsadas(limit: Int)` - Top etiquetas
7. `reportesPorUsuario(usuario: ID!)` - Reportes de un usuario
8. `actividadReciente(limit: Int)` - Actividad mezclada
9. `usuariosMasActivos(limit: Int)` - Top usuarios
10. `reportesPorEstado(estado: String!)` - Filtrar por estado
11. `reportesPorFecha(desde: String!, hasta: String!)` - Filtrar por rango

**Query compuesta con PDF:**

```graphql
query {
  reportAnalytics(reporteId: "1", formato: "pdf") {
    reporte {
      title
    }
    comentarios {
      content
    }
    pdfBase64 # PDF en base64
  }
}
```

**Playground:** http://localhost:4000/graphql

---

### WebSocket Eventos

**Conexión:**

```
ws://localhost:8080/ws?room=reports&token=<JWT>
```

**Eventos recibidos (server → client):**

```json
{
  "type": "new_report",
  "message": "Nuevo reporte creado: #123",
  "data": {
    "report_id": 123,
    "title": "Problema en servidor",
    "created_at": "2025-10-29T10:30:00Z"
  }
}
```

**Ping/Pong (keep-alive):**

```json
// Client → Server
{ "type": "ping" }

// Server → Client
{ "type": "pong", "timestamp": 1698582600 }
```

---

## 📅 Evolución del diseño por semana

**Semana 3:** Definición de arquitectura inicial y stack tecnológico  
**Semana 4:** Implementación de REST API y setup de base de datos  
**Semana 5:** Integración de GraphQL y WebSocket, primer frontend funcional  
**Semana 6:** Queries analíticas, exportación PDF, mejoras de UI/UX  
**Semana 7:** Tests E2E, optimización, documentación completa

---

## 🔧 Herramientas de desarrollo

- **Postman/Insomnia:** Para probar endpoints REST
- **GraphQL Playground:** Incluido en Apollo Server
- **wscat:** Para probar WebSocket desde CLI
  ```bash
  npm install -g wscat
  wscat -c "ws://localhost:8080/ws?room=reports"
  ```
- **pgAdmin:** Para administrar base de datos PostgreSQL

---

## 📖 Documentación adicional

- **REST API:** Ver `sistema_de_informes/services/rest-api/README.md` (Semanas 3-7)
- **GraphQL:** Ver `sistema_de_informes/services/graphql/README.md` (Semanas 3-7)
- **WebSocket:** Ver `sistema_de_informes/services/ws/README.md` (Semanas 3-7)
- **Frontend:** Ver `sistema_de_informes/apps/frontend/README.md` (Semanas 5-7)
- **Scripts:** Ver `sistema_de_informes/scripts/README.md`

---

**Documentación completa — Sistema totalmente documentado para evaluación del docente.**
