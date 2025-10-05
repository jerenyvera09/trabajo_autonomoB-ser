# 🌐 Sistema de Reportes de Infraestructura Universitaria

## 🏛 Universidad Laica Eloy Alfaro de Manabí

**Facultad:** Ciencias de la Vida y Tecnologías  
**Carrera:** Ingeniería de Software  
**Asignatura:** Aplicación para el Servidor Web  
**Docente:** John Cevallos

---

## 👥 Integrantes del Grupo

- **Vera Mero Jereny Jhonnayker**
- **Zambrano Gavilanes Cinthia Dayanna**
- **Delgado Campuzano Carlos Alberto**

---

## 📖 Descripción general

El **Sistema de Reportes de Infraestructura Universitaria** es una aplicación web diseñada para gestionar y dar seguimiento a reportes de incidentes en la comunidad universitaria (daños en infraestructura, problemas de seguridad, necesidades de mantenimiento, etc.).

Los reportes pueden incluir **archivos adjuntos (imágenes, videos)**, clasificarse por **categorías y estados**, y mencionar a **autoridades o áreas responsables** mediante etiquetas y menciones para mejorar la atención y trazabilidad.

---

## 🎯 Objetivo general

Construir un **sistema distribuido** que demuestre competencias en desarrollo full-stack: APIs REST y GraphQL, comunicación en tiempo real (WebSockets), integración entre servicios y una interfaz de usuario interactiva.

---

## ⚙️ Arquitectura del sistema

La solución propuesta es modular y distribuida, con los siguientes componentes principales:

1. **Servicio REST (backend principal)**
   - CRUD de las entidades principales
   - Autenticación y autorización
   - Validaciones y manejo de errores

2. **Servicio GraphQL**
   - Consultas y agregaciones avanzadas
   - Integración con el backend REST

3. **Servidor WebSocket**
   - Notificaciones y actualizaciones en tiempo real
   - Canales para comunicación entre usuarios y autoridades

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
