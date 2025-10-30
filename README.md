# 🌐 Sistema de Reportes de Infraestructura Universitaria

**Proyecto Final - Semana 7**  
Sistema distribuido con arquitectura de microservicios para gestión de reportes universitarios con notificaciones en tiempo real.

[![Estado](https://img.shields.io/badge/Estado-Completado-success)](https://github.com/jerenyvera09/trabajo_autonomoB-ser)
[![Semana](https://img.shields.io/badge/Semana-7-blue)](https://github.com/jerenyvera09/trabajo_autonomoB-ser)
[![Fecha](https://img.shields.io/badge/Fecha-29%2F10%2F2025-orange)](https://github.com/jerenyvera09/trabajo_autonomoB-ser)

---

## 📋 Tabla de Contenidos

- [🏛️ Información Académica](#️-información-académica)
- [👥 Equipo de Desarrollo](#-equipo-de-desarrollo)
- [🎯 Descripción del Proyecto](#-descripción-del-proyecto)
- [🏗️ Arquitectura](#️-arquitectura)
- [🚀 Inicio Rápido](#-inicio-rápido)
- [📚 Documentación Semanal](#-documentación-semanal)
- [🔗 Enlaces Importantes](#-enlaces-importantes)
- [📊 Evidencias](#-evidencias)
- [📝 Changelog](#-changelog)

---

## 🏛️ Información Académica

**Universidad:** Laica Eloy Alfaro de Manabí (ULEAM)  
**Facultad:** Ciencias de la Vida y Tecnologías  
**Carrera:** Ingeniería de Software  
**Asignatura:** Aplicación para el Servidor Web  
**Docente:** Ing. John Cevallos  
**Semestre:** 2024-2025 - 5to Semestre "B"  
**Fecha de entrega:** 29 de octubre de 2025

---

## 👥 Equipo de Desarrollo

| Integrante                             | Responsabilidad                     | Stack Tecnológico                       | Documentación                                            |
| -------------------------------------- | ----------------------------------- | --------------------------------------- | -------------------------------------------------------- |
| **Cinthia Dayanna Zambrano Gavilanes** | REST API + Base de Datos            | Python, FastAPI, SQLAlchemy, PostgreSQL | [📄 Ver READMEs](sistema_de_informes/services/rest-api/) |
| **Carlos Alberto Delgado Campuzano**   | GraphQL Server + Queries Analíticas | TypeScript, Apollo Server, GraphQL      | [📄 Ver READMEs](sistema_de_informes/services/graphql/)  |
| **Jereny Jhonnayker Vera Mero**        | WebSocket Server + Notificaciones   | Go, Gorilla WebSocket, JSON             | [📄 Ver READMEs](sistema_de_informes/services/ws/)       |
| **Equipo Completo**                    | Frontend + Integración              | React, TypeScript, Vite, Apollo Client  | [📄 Ver READMEs](sistema_de_informes/apps/frontend/)     |

---

## 🎯 Descripción del Proyecto

El **Sistema de Reportes de Infraestructura Universitaria** es una aplicación web completa diseñada para gestionar reportes de incidentes en la comunidad universitaria (daños en infraestructura, problemas de seguridad, necesidades de mantenimiento, etc.).

### ✨ Características Principales

- ✅ **CRUD Completo** - Crear, leer, actualizar y eliminar reportes
- ✅ **Autenticación JWT** - Login seguro con tokens
- ✅ **Queries Avanzadas** - 11 queries analíticas con GraphQL
- ✅ **Notificaciones en Tiempo Real** - WebSocket con sistema de rooms
- ✅ **Exportación a PDF** - Generación de reportes en PDF
- ✅ **Interfaz Moderna** - React + TypeScript con diseño responsivo
- ✅ **Integración Completa** - 3 servicios backend + frontend trabajando juntos

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────┐
│          FRONTEND (React + TypeScript)              │
│             http://localhost:3000                   │
│  - UI Responsiva con notificaciones en tiempo real │
│  - Apollo Client para GraphQL                      │
│  - WebSocket para actualizaciones live             │
└──────────┬──────────────┬──────────────┬───────────┘
           │              │              │
           ▼              ▼              ▼
   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
   │  REST API    │ │   GraphQL    │ │  WebSocket   │
   │  FastAPI     │◄┤   Apollo     │ │   Gorilla    │
   │  Port: 8000  │ │   Port: 4000 │ │   Port: 8080 │
   │              │ │              │ │              │
   │ - CRUD       │ │ - Queries    │ │ - Rooms      │
   │ - Auth JWT   │ │ - Analytics  │ │ - Ping/Pong  │
   │ - Validación │ │ - PDF Export │ │ - Auth Token │
   └──────┬───────┘ └──────────────┘ └──────────────┘
          │
          ▼
   ┌──────────────┐
   │  PostgreSQL  │
   │  (Supabase)  │
   │  10 Tablas   │
   └──────────────┘
```

**Stack Tecnológico:**

- **Backend:** Python (FastAPI), TypeScript (Apollo Server), Go (Gorilla)
- **Frontend:** React 18, TypeScript, Vite, Apollo Client
- **Base de Datos:** PostgreSQL (Supabase)
- **Autenticación:** JWT (JSON Web Tokens)
- **Notificaciones:** WebSocket (Gorilla)

---

## 🚀 Inicio Rápido

### Prerequisitos

- Python 3.11+
- Node.js 18+
- Go 1.21+
- PostgreSQL (o cuenta en Supabase)

### Instalación y Ejecución

**Opción 1 - Ejecución manual (4 terminales):**

```bash
# Terminal 1 - REST API
cd sistema_de_informes/services/rest-api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 - GraphQL
cd sistema_de_informes/services/graphql
npm install
npm run dev

# Terminal 3 - WebSocket
cd sistema_de_informes/services/ws
go run main.go

# Terminal 4 - Frontend
cd sistema_de_informes/apps/frontend
npm install
npm run dev
```

**Servicios disponibles:**

- 🌐 Frontend: http://localhost:3000
- 🔌 REST API: http://localhost:8000 ([Docs](http://localhost:8000/docs))
- 📊 GraphQL: http://localhost:4000/graphql
- 🔔 WebSocket: ws://localhost:8080/ws?room=reports

---

## 📚 Documentación Semanal

Cada servicio tiene documentación detallada por semana mostrando el progreso incremental:

### 🐍 REST API (Python/FastAPI)

- [📄 Semana 3](sistema_de_informes/services/rest-api/README.md) - Setup y arquitectura
- [📄 Semana 4](sistema_de_informes/services/rest-api/README_SEMANA4.md) - CRUD básico y autenticación
- [📄 Semana 5](sistema_de_informes/services/rest-api/README_SEMANA5.md) - Integración con WebSocket
- [📄 Semana 6](sistema_de_informes/services/rest-api/README_SEMANA6.md) - Validaciones y tests E2E
- [📄 Semana 7](sistema_de_informes/services/rest-api/README_SEMANA7.md) - Documentación final y demo

### 📊 GraphQL (TypeScript/Apollo)

- [📄 Semana 3](sistema_de_informes/services/graphql/README.md) - Setup y arquitectura
- [📄 Semana 4](sistema_de_informes/services/graphql/README_SEMANA4.md) - Resolvers básicos
- [📄 Semana 5](sistema_de_informes/services/graphql/README_SEMANA5.md) - Queries de interacción
- [📄 Semana 6](sistema_de_informes/services/graphql/README_SEMANA6.md) - 11 queries analíticas + PDF
- [📄 Semana 7](sistema_de_informes/services/graphql/README_SEMANA7.md) - Tests y documentación

### 🔔 WebSocket (Go/Gorilla)

- [📄 Semana 3](sistema_de_informes/services/ws/README.md) - Setup y arquitectura
- [📄 Semana 4](sistema_de_informes/services/ws/README_SEMANA4.md) - Sistema de rooms
- [📄 Semana 5](sistema_de_informes/services/ws/README_SEMANA5.md) - Ping/Pong y autenticación
- [📄 Semana 6](sistema_de_informes/services/ws/README_SEMANA6.md) - Tests de integración
- [📄 Semana 7](sistema_de_informes/services/ws/README_SEMANA7.md) - Dashboard y documentación

### 🖥️ Frontend (React/TypeScript)

- [📄 Semana 5](sistema_de_informes/apps/frontend/README.md) - Setup e integración triple
- [📄 Semana 6](sistema_de_informes/apps/frontend/README_SEMANA6.md) - CRUD completo y autenticación
- [📄 Semana 7](sistema_de_informes/apps/frontend/README_SEMANA7.md) - Tests E2E y optimización

### 📖 Documentación Adicional

- [📚 Índice de Docs](sistema_de_informes/docs/README.md) - Arquitectura, diagramas, contratos
- [🔧 Scripts](sistema_de_informes/scripts/README.md) - Automatización y testing

---

## 🔗 Enlaces Importantes

- **Documentación Interactiva:**
  - REST API Swagger: http://localhost:8000/docs
  - GraphQL Playground: http://localhost:4000/graphql
- **Repositorio GitHub:**
  - Código fuente: https://github.com/jerenyvera09/trabajo_autonomoB-ser
- **Diagramas:**
  - [Arquitectura del Sistema](sistema_de_informes/docs/arquitectura.png)
  - [Diagrama UML](sistema_de_informes/docs/uml.png)

---

## 📊 Evidencias

### Distribución de Commits por Integrante

```bash
# Ver commits por autor
git shortlog -sn --all

# Resultado:
# 14  Jereny Vera       (WebSocket + Coordinación)
#  7  Carlos Campuzano  (GraphQL)
#  2  Cinthia Zambrano  (REST API)
```

### Commits por Semana

- **Semana 3:** Setup inicial y arquitectura
- **Semana 4:** Implementación de servicios básicos
- **Semana 5:** Integración entre servicios
- **Semana 6:** Queries analíticas y funcionalidades avanzadas
- **Semana 7:** Tests, optimización y documentación completa

---

## 📝 Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para historial completo de cambios por semana.

---

## 🎓 Objetivos de Aprendizaje Alcanzados

### ✅ Competencias Técnicas

1. **Desarrollo Backend Polyglot:**
   - Python (FastAPI) para REST API con validaciones Pydantic
   - TypeScript (Apollo Server) para GraphQL con resolvers modulares
   - Go (Gorilla) para WebSocket con concurrencia eficiente

2. **Integración de Servicios:**
   - Comunicación REST → GraphQL (DataSources)
   - Notificaciones REST → WebSocket
   - Frontend → 3 backends simultáneos

3. **Autenticación y Seguridad:**
   - JWT para autenticación
   - Validación de tokens en WebSocket
   - CORS configurado correctamente

4. **Testing y Calidad:**
   - Tests E2E con pytest
   - Tests de integración entre servicios
   - Validación de comportamiento

### ✅ Buenas Prácticas Aplicadas

- ✅ Código modular y reutilizable
- ✅ Documentación completa por semanas
- ✅ Variables de entorno para configuración
- ✅ Manejo estructurado de errores
- ✅ Commits descriptivos y frecuentes
- ✅ READMEs profesionales con ejemplos

---

## 📸 Screenshots (Opcional)

> Agregar en `docs/evidencias/` capturas de pantalla del sistema funcionando

---

## 🤝 Contribuciones

Este proyecto fue desarrollado como parte de la asignatura **Aplicación para el Servidor Web**.

**Metodología de trabajo:**

- Reuniones semanales de coordinación
- Commits individuales por responsabilidad
- Revisiones de código entre pares
- Documentación incremental por semana

---

## 📄 Licencia

Este proyecto es académico y fue desarrollado para fines educativos en la ULEAM.

---

## 🙏 Agradecimientos

- **Docente:** Ing. John Cevallos - Por la guía y enseñanzas durante el semestre
- **Universidad ULEAM** - Por la formación académica
- **Equipo de desarrollo** - Por el trabajo colaborativo

---

**✨ Proyecto completado exitosamente - Semana 7 - 29/10/2025 ✨**

**Facultad:** Ciencias de la Vida y Tecnologías  
**Carrera:** Ingeniería de Software  
**Asignatura:** Aplicación para el Servidor Web  
**Docente:** John Cevallos  
**Semestre:** 2024-2025 5to Semestre "B"  
**Semana:** 6 (Commit 4) - Integración Completa, Dashboard y Documentación Final

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

## ⚙️ Arquitectura del sistema (Semana 6)

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
- Dashboard interactivo (listas REST/GraphQL + KPIs)

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

## 🧪 Pruebas de integración (Semana 6)

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
    items {
      id
      title
      description
      status
      priority
    }
    total
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

Para cambios de reporte (Semana 6), también puedes enviar:

```bash
curl -X POST http://localhost:8080/notify/reports \
  -H "Content-Type: application/json" \
  -d '{"event":"update_report","message":"Reporte actualizado"}'
```

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

## ✅ Funcionalidades completadas (Semana 6)

### REST API

- [x] CRUD completo de 10 entidades
- [x] Autenticación JWT
- [x] Endpoint `/api/v1/reports` para integración
- [x] CORS habilitado
- [x] Validaciones y manejo de errores

### GraphQL

- [x] Schema con tipos Report
- [x] Query `reports` que consume REST
- [x] `report(id)` y `reportsAnalytics` (KPIs)
- [x] Playground interactivo
- [x] Manejo de errores

### WebSocket

- [x] Conexión WebSocket bidireccional
- [x] Broadcast a todos los clientes y por salas
- [x] Endpoint POST `/notify` para eventos (incluye `update_report`)
- [x] Detección de evento `new_report`
- [x] Keepalive ping/pong

### Frontend

- [x] Integración con REST API
- [x] Integración con GraphQL
- [x] Conexión WebSocket persistente
- [x] Notificaciones en tiempo real
- [x] Dashboard interactivo (listas + KPIs GraphQL)
- [x] Diseño responsivo

---

## 📝 Commits realizados

- **Commit 1 (Semana 3)**: Diseño de BD y esquema inicial
- **Commit 2 (Semana 4)**: Implementación de servicios individuales
- **Commit 3 (Semana 5)**: Integración completa y frontend
- **Commit 4 (Semana 6)**: Dashboard con KPIs, handlers de errores, docs finales ✅ ACTUAL

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

✅ **Proyecto listo para evaluación - Semana 6 (Commit 4)**  
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

## � Capturas del Dashboard

Coloca las capturas en `sistema_de_informes/docs/dashboard_capturas/` con estos nombres sugeridos (o ajusta):

- `01_lista_rest.png` — Lista de reportes desde REST
- `02_lista_graphql.png` — Lista de reportes desde GraphQL
- `03_notificacion_ws.png` — Notificación WS en tiempo real
- `04_estadisticas_kpis.png` — KPIs de `reportsAnalytics`

Luego, enlázalas aquí para la presentación final.

## 🚀 Comandos de ejecución (resumen)

En cuatro terminales separadas (Windows CMD):

```cmd
cd sistema_de_informes\services\rest-api & uvicorn main:app --reload --port 8000
```

```cmd
cd sistema_de_informes\services\graphql & npm install & npm run dev
```

```cmd
cd sistema_de_informes\services\ws & go run main.go
```

```cmd
cd sistema_de_informes\apps\frontend & npm install & npm run dev
```

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

---

## ✅ Verificación de Cumplimiento 100%

### **Requisitos del Docente (Audio + PDF)**

| #   | Requisito                                    | Estado      | Evidencia                                                                      |
| --- | -------------------------------------------- | ----------- | ------------------------------------------------------------------------------ |
| 1️⃣  | **GraphQL conectado a REST**                 | ✅ COMPLETO | `services/graphql/src/datasources/rest.ts` - RestDataSource con 11 métodos GET |
| 2️⃣  | **11 queries analíticas (3 por integrante)** | ✅ COMPLETO | `services/graphql/src/resolvers/analytics.ts` - 11 queries documentadas        |
| 3️⃣  | **Frontend consume queries analíticas**      | ✅ COMPLETO | `apps/frontend/src/App.tsx` - Dashboard con KPIs (línea 456-575)               |
| 4️⃣  | **Reportes PDF descargables**                | ✅ COMPLETO | `services/graphql/src/resolvers/export.ts` + botones en App.tsx                |
| 5️⃣  | **Dashboard con gráficos en tiempo real**    | ✅ COMPLETO | `apps/frontend/src/App.tsx` - 4 KPIs + Top Áreas + Promedio                    |
| 6️⃣  | **REST → WebSocket notificaciones**          | ✅ COMPLETO | `services/rest-api/ws_notifier.py` - 3 funciones activas                       |
| 7️⃣  | **WebSocket → Frontend actualización**       | ✅ COMPLETO | `apps/frontend/src/App.tsx` - Conexión WS (línea 345)                          |
| 8️⃣  | **Distribución por integrante documentada**  | ✅ COMPLETO | `services/graphql/README.md` - Sección "Distribución de Queries"               |
| 9️⃣  | **Sin duplicar CRUD en GraphQL**             | ✅ COMPLETO | GraphQL solo consulta, no crea/actualiza/elimina                               |
| 🔟  | **Integración completa visible**             | ✅ COMPLETO | Dashboard muestra REST + GraphQL + WebSocket juntos                            |

---

### **Funcionalidades Implementadas**

#### **📊 Dashboard Analítico (NEW)**

- ✅ **4 KPIs principales**: Total, Abiertos, En Proceso, Cerrados
- ✅ **Top 3 Áreas**: Con ranking visual (🥇🥈🥉)
- ✅ **Promedio Puntuaciones**: Con indicador de calidad
- ✅ **Actualización automática**: Vía WebSocket en tiempo real

#### **📄 Reportes PDF (NEW)**

- ✅ **Botón en cada reporte**: "Descargar Reporte PDF"
- ✅ **Query GraphQL**: `reportAnalytics(reporteId, formato: "pdf")`
- ✅ **Generación con pdfkit**: 6 secciones (reporte, usuario, categoría, comentarios, puntuaciones, archivos)
- ✅ **Descarga directa**: Base64 → PDF descargable en navegador

#### **🔗 Integración Completa**

- ✅ **REST API**: 10 entidades CRUD
- ✅ **GraphQL**: 11 queries analíticas consumiendo REST
- ✅ **WebSocket**: 3 eventos en tiempo real
- ✅ **Frontend**: Consume las 3 tecnologías simultáneamente

---

### **Distribución Individual de Trabajo**

| Integrante           | Queries Analíticas                                                         | Archivo                  | Líneas  |
| -------------------- | -------------------------------------------------------------------------- | ------------------------ | ------- |
| **Cinthia Zambrano** | statsReportes, reportesPorArea, topAreas                                   | analytics.ts             | 50-100  |
| **Carlos Campuzano** | reportesPorCategoria, promedioPuntuaciones, etiquetasMasUsadas             | analytics.ts             | 100-150 |
| **Jereny Vera**      | reportesPorUsuario, actividadReciente, usuariosMasActivos, reportAnalytics | analytics.ts + export.ts | 150-224 |

---

## 📚 Referencias Oficiales

### **Tecnologías Utilizadas**

| Tecnología                           | Documentación Oficial                             |
| ------------------------------------ | ------------------------------------------------- |
| **FastAPI** (REST API)               | https://fastapi.tiangolo.com/                     |
| **Apollo Server** (GraphQL)          | https://www.apollographql.com/docs/apollo-server/ |
| **Gorilla WebSocket** (WebSocket Go) | https://github.com/gorilla/websocket              |
| **React** (Frontend)                 | https://react.dev/                                |
| **TypeScript**                       | https://www.typescriptlang.org/docs/              |
| **PostgreSQL**                       | https://www.postgresql.org/docs/                  |
| **Supabase**                         | https://supabase.com/docs                         |

### **Librerías y Herramientas**

| Librería                              | Documentación                 |
| ------------------------------------- | ----------------------------- |
| **SQLAlchemy** (ORM Python)           | https://docs.sqlalchemy.org/  |
| **pdfkit** (Generación PDF)           | https://pdfkit.org/           |
| **httpx** (Cliente HTTP async Python) | https://www.python-httpx.org/ |
| **Vite** (Build tool)                 | https://vitejs.dev/           |

---

**Sistema de Informes Universidad - Semana 6** 🚀  
**Cumplimiento 100%** con requisitos del docente ✅
