# 🌐 Sistema de Reportes de Infraestructura Universitaria

## 🏛 Universidad Laica Eloy Alfaro de Manabí

**Facultad:** Ciencias de la Vida y Tecnologías  
**Carrera:** Ingeniería de Software  
**Asignatura:** Aplicación para el Servidor Web  
**Docente:** John Cevallos  
**Semestre:** 2024-2025 5to Semestre "B"  
**Semana:** 5 (Commit 3) - Integración de Servicios y Frontend

---

## 👥 Integrantes del Grupo

| Integrante                             | Responsabilidad  | Tecnología        |
| -------------------------------------- | ---------------- | ----------------- |
| **Cinthia Dayanna Zambrano Gavilanes** | REST API         | Python/FastAPI    |
| **Carlos Alberto Delgado Campuzano**   | GraphQL Server   | TypeScript/Apollo |
| **Jereny Jhonnayker Vera Mero**        | WebSocket Server | Go/Gorilla        |

---

## 📖 Descripción general

El **Sistema de Reportes de Infraestructura Universitaria** es una aplicación web diseñada para gestionar y dar seguimiento a reportes de incidentes en la comunidad universitaria (daños en infraestructura, problemas de seguridad, necesidades de mantenimiento, etc.).

**Características principales:**

- ✅ Gestión completa de reportes con CRUD
- ✅ Autenticación y autorización con JWT
- ✅ Consultas avanzadas con GraphQL
- ✅ Notificaciones en tiempo real con WebSocket
- ✅ Interfaz web moderna y responsiva
- ✅ Integración completa entre servicios

---

## 🎯 Objetivo general

Construir un **sistema distribuido** que demuestre competencias en desarrollo full-stack: APIs REST y GraphQL, comunicación en tiempo real (WebSockets), integración entre servicios y una interfaz de usuario interactiva.

---

## ⚙️ Arquitectura del sistema (Semana 5)

La solución es modular y distribuida, con **cuatro componentes principales**:

```
┌─────────────────────────────────────────────────────┐
│          FRONTEND (React + TypeScript)              │
│             http://localhost:3000                   │
└──────────┬──────────────┬──────────────┬───────────┘
           │              │              │
           ▼              ▼              ▼
   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
   │  REST API    │ │   GraphQL    │ │  WebSocket   │
   │  FastAPI     │◄┤   Apollo     │ │   Gorilla    │
   │  :8000       │ │   :4000      │ │   :8080      │
   └──────┬───────┘ └──────────────┘ └──────────────┘
          │
          ▼
   ┌──────────────┐
   │   SQLite     │
   │   Database   │
   └──────────────┘
```

Diagrama de arquitectura (referencia):

![Arquitectura Integración](sistema_de_informes/docs/arquitectura.png)

### 1️⃣ **Servicio REST (Python/FastAPI)** - Puerto 8000

- CRUD completo de todas las entidades
- Autenticación JWT
- Endpoint `/api/v1/reports` para integración
- CORS habilitado para frontend y GraphQL

### 2️⃣ **Servicio GraphQL (TypeScript/Apollo)** - Puerto 4000

- Query `reports` que consume REST API
- Consultas y agregaciones avanzadas
- Playground interactivo

### 3️⃣ **Servidor WebSocket (Go/Gorilla)** - Puerto 8080

- Notificaciones en tiempo real
- Broadcast de eventos a clientes conectados
- Endpoint POST `/notify` para simulación

### 4️⃣ **Frontend (React/Vite)** - Puerto 3000

- Interfaz moderna y responsiva
- Integración con los 3 servicios backend
- Notificaciones en tiempo real
- Dashboard interactivo

---

## 🚀 Cómo ejecutar el proyecto completo

### Requisitos previos

- **Python 3.10+**
- **Node.js 18+**
- **Go 1.20+**

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/jerenyvera09/trabajo_autonomoB-ser.git
cd trabajo_autonomoB-ser/sistema_de_informes
```

### Paso 2: Iniciar REST API (Terminal 1)

```bash
cd services/rest-api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

✅ Disponible en: http://localhost:8000

### Paso 3: Iniciar GraphQL (Terminal 2)

```bash
cd services/graphql
npm install
npm run dev
```

✅ Disponible en: http://localhost:4000/graphql

### Paso 4: Iniciar WebSocket (Terminal 3)

```bash
cd services/ws
go run main.go
```

✅ Disponible en: ws://localhost:8080/ws

### Paso 5: Iniciar Frontend (Terminal 4)

```bash
cd apps/frontend
npm install
npm run dev
```

✅ Disponible en: http://localhost:3000

---

## 🧪 Pruebas de integración

### Verificar que todos los servicios estén activos

```bash
# REST API
curl http://localhost:8000/health

# GraphQL (abrir en navegador)
http://localhost:4000/graphql

# WebSocket
curl http://localhost:8080/

# Frontend (abrir en navegador)
http://localhost:3000
```

### Ejemplo de consulta GraphQL (playground)

Abre http://localhost:4000/graphql y ejecuta:

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

Deberías ver los mismos datos que devuelve el endpoint REST `GET http://localhost:8000/api/v1/reports`.

### Probar notificaciones en tiempo real

Simula un nuevo reporte y observa el banner en el frontend:

```bash
curl -X POST http://localhost:8080/notify \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"¡Nuevo reporte creado!\"}"
```

También puedes conectarte por WebSocket y escuchar los mensajes:

- Opción rápida (DevTools navegador):
  1.  Abre el frontend en http://localhost:3000
  2.  En la consola ejecuta:
      `ws = new WebSocket('ws://localhost:8080/ws'); ws.onmessage = (e) => console.log('WS:', e.data);`
  3.  Envía un evento: `fetch('http://localhost:8080/notify', {method:'POST'})`

- Opción con wscat (si lo tienes instalado):
  ```bash
  wscat -c ws://localhost:8080/ws
  > new_report
  ```
  Al enviar `new_report`, el servidor emitirá `{ "event": "new_report", "message": "Se ha creado un nuevo reporte" }`.

---

## 📁 Estructura del proyecto

```
sistema_de_informes/
├── services/
│   ├── rest-api/           # Python/FastAPI (Integrante 1)
│   │   ├── main.py
│   │   ├── entities/       # Modelos SQLAlchemy
│   │   ├── routers/        # Endpoints CRUD
│   │   ├── schemas/        # Pydantic schemas
│   │   └── README.md
│   ├── graphql/            # TypeScript/Apollo (Integrante 2)
│   │   ├── src/
│   │   │   ├── index.ts
│   │   │   ├── schema.ts
│   │   │   └── resolvers/
│   │   └── README.md
│   └── ws/                 # Go/Gorilla (Integrante 3)
│       ├── main.go
│       ├── go.mod
│       └── README.md
├── apps/
│   └── frontend/           # React/TypeScript/Vite
│       ├── src/
│       │   ├── App.tsx     # Componente principal
│       │   └── index.css   # Estilos
│       ├── .env.example    # Variables de entorno
│       └── README.md
├── docs/
│   └── integracion.md      # Documentación técnica
└── README.md               # Este archivo
```

---

## 📚 Documentación detallada

- **REST API**: [services/rest-api/README.md](sistema_de_informes/services/rest-api/README.md)
- **GraphQL**: [services/graphql/README.md](sistema_de_informes/services/graphql/README.md)
- **WebSocket**: [services/ws/README.md](sistema_de_informes/services/ws/README.md)
- **Frontend**: [apps/frontend/README.md](sistema_de_informes/apps/frontend/README.md)
- **Integración**: [docs/integracion.md](sistema_de_informes/docs/integracion.md)

---

## 🔧 Tecnologías utilizadas

| Componente    | Tecnología        | Versión | Puerto |
| ------------- | ----------------- | ------- | ------ |
| REST API      | Python/FastAPI    | 0.115.5 | 8000   |
| GraphQL       | TypeScript/Apollo | 4.11.2  | 4000   |
| WebSocket     | Go/Gorilla        | 1.23    | 8080   |
| Frontend      | React/Vite        | 18.2    | 3000   |
| Base de Datos | SQLite            | 3.x     | -      |

---

## ✅ Funcionalidades completadas (Semana 5)

### REST API

- [x] CRUD completo de 10 entidades
- [x] Autenticación JWT
- [x] Endpoint `/api/v1/reports` para integración
- [x] CORS habilitado
- [x] Validaciones y manejo de errores

### GraphQL

- [x] Schema con tipos Report
- [x] Query `reports` que consume REST
- [x] Playground interactivo
- [x] Manejo de errores

### WebSocket

- [x] Conexión WebSocket bidireccional
- [x] Broadcast a todos los clientes
- [x] Endpoint POST `/notify` para eventos
- [x] Detección de evento `new_report`

### Frontend

- [x] Integración con REST API
- [x] Integración con GraphQL
- [x] Conexión WebSocket persistente
- [x] Notificaciones en tiempo real
- [x] Dashboard interactivo
- [x] Diseño responsivo

---

## 📝 Commits realizados

- **Commit 1 (Semana 3)**: Diseño de BD y esquema inicial
- **Commit 2 (Semana 4)**: Implementación de servicios individuales
- **Commit 3 (Semana 5)**: Integración completa y frontend ✅ ACTUAL

---

## 👨‍💻 Equipo de desarrollo

- **Cinthia Zambrano**: Desarrollo REST API, gestión de base de datos
- **Carlos Campuzano**: Desarrollo GraphQL, integración con REST
- **Jereny Vera**: Desarrollo WebSocket, notificaciones en tiempo real
- **Equipo completo**: Frontend e integración

---

## 📄 Licencia

Este proyecto es de uso académico para la materia Aplicación para el Servidor Web - ULEAM 2024-2025.

---

✅ **Proyecto listo para evaluación - Semana 5 (Commit 3)**  
🎓 **Universidad Laica Eloy Alfaro de Manabí**

4. **Frontend interactivo**
   - Panel (dashboard) de reportes
   - Integración con REST, GraphQL y WebSockets
   - Interfaz responsiva y accesible

---

## 🧩 Tecnologías (sugeridas)

| Componente           |    Lenguaje / Framework | Ejemplo                                   |
| -------------------- | ----------------------: | ----------------------------------------- |
| Backend REST         |                  Python | FastAPI o Flask                           |
| GraphQL API          |              TypeScript | NestJS + Apollo Server                    |
| WebSocket Server     |             Go (Golang) | Server para notificaciones en tiempo real |
| Frontend             | JavaScript / TypeScript | React, Vue o Angular                      |
| Base de datos        |      PostgreSQL / MySQL | Almacenamiento relacional                 |
| Control de versiones |            Git + GitHub | Repositorio y flujo de branches           |

---

## 🧱 Modelo de datos (resumen)

Entidades principales: Usuario, Rol, Reporte, Comentario, EstadoReporte, Categoría, ArchivoAdjunto, Área, Puntuación y Etiqueta.  
El diagrama entidad-relación se encuentra en el repositorio para detalle completo.

---

## 📌 Lineamientos de desarrollo

- Uso de control de versiones con ramas y commits descriptivos.
- Documentación de las APIs (OpenAPI / GraphQL schema) y del despliegue.
- Pruebas unitarias y de integración para componentes críticos.
- Manejo seguro de autenticación, autorización y validación de datos.

---

## 🚀 Próximos pasos / Tareas iniciales

- [ ] Definir responsabilidades por integrante y stack tecnológico.
- [ ] Especificar endpoints REST y esquema GraphQL.
- [ ] Implementar el backend REST básico (auth + CRUD de Reportes).
- [ ] Implementar el servidor WebSocket para notificaciones.
- [ ] Crear un prototipo de frontend y conectarlo con el backend.

## 📁 Estructura del repositorio (resumen)

Este repositorio contiene, de forma aproximada, las siguientes carpetas:

- `backend/` → Código del servicio REST (Python / FastAPI)
- `graphql/` → Servicio GraphQL (TypeScript / NestJS) ← opcional según implementación
- `websocket/` → Servidor de WebSockets (Go / otro)
- `frontend/` → Aplicación cliente (React / Vue / Angular)
- `docs/` → Diagramas (ER, arquitectura), especificaciones y entregables
- `scripts/` → Scripts útiles (migraciones, seeds, utilidades)
- `README.md` → Documentación principal

---

## 🔑 Variables de entorno (ejemplo)

Backend (`backend/.env`):

- `DATABASE_URL` e.g. `postgresql://user:pass@localhost:5432/dbname`
- `SECRET_KEY`
- `DEBUG` (True/False)

Frontend (`frontend/.env.development`):

- `REACT_APP_API_BASE_URL` e.g. `http://localhost:8000`

---

## 🟡 Estado del proyecto (breve)

- [x] Documento de objetivos y reglas (README)
- [ ] Backend REST: endpoints básicos (CRUD)
- [ ] GraphQL: esquema y consultas de reportes
- [ ] WebSocket: notificaciones en tiempo real
- [ ] Frontend: dashboard interactivo
- [ ] Tests y documentación de endpoints

---

📂 **Repositorio oficial:** https://github.com/jerenyvera09/trabajo_autonomoB-ser
