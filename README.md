# 🌐 Sistema de Reportes Infraestructura Univercitaria

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

## 📖 Descripción General

El **Sistema de Reportes de infraestructura univercitaria** es una aplicación web orientada a la gestión y seguimiento de reportes realizados por los usuarios sobre incidentes en la comunidad (como daños de infraestructura, problemas públicos, entre otros).  

Los reportes pueden incluir **archivos adjuntos (imágenes, videos)**, ser clasificados por **categorías y estados**, y etiquetar a **autoridades o áreas responsables** mediante un sistema de **etiquetas y menciones**, mejorando así la visibilidad y atención de cada caso.

---

## 🎯 Objetivo General del Proyecto

Desarrollar un **sistema distribuido completo**, aplicando múltiples tecnologías y lenguajes de programación para demostrar competencias en **arquitectura full-stack, integración de servicios REST, GraphQL y WebSockets**, junto con un **frontend interactivo** y **funcionalidades en tiempo real**.

---

## ⚙️ Arquitectura del Sistema

El sistema se desarrollará bajo una **arquitectura distribuida**, compuesta por los siguientes módulos:

1. **Servicio REST (Backend Principal)**  
   - CRUD de entidades principales  
   - Autenticación y autorización  
   - Validaciones y manejo de errores  

2. **Servicio GraphQL**  
   - Consultas avanzadas de reportes y análisis de datos  
   - Integración con el servicio REST  

3. **Servidor WebSocket**  
   - Notificaciones y actualizaciones en tiempo real  
   - Canales para comunicación entre usuarios y autoridades  

4. **Frontend Interactivo**  
   - Dashboard de reportes  
   - Integración con REST, GraphQL y WebSockets  
   - Interfaz adaptable y dinámica  

---

## 🧩 Tecnologías Principales

| Componente | Lenguaje / Framework | Descripción |
|-------------|----------------------|--------------|
| Backend REST | **Python (FastAPI / Flask)** | Gestión principal del sistema y autenticación |
| GraphQL API | **TypeScript (NestJS + Apollo Server)** | Consultas y mutaciones complejas |
| WebSocket Server | **Go (Golang)** | Comunicación y notificaciones en tiempo real |
| Frontend | **React / Vue / Angular** | Dashboard e interacción con usuarios |
| Base de Datos | **PostgreSQL / MySQL** | Almacenamiento de datos relacionales |
| Control de Versiones | **Git + GitHub** | Repositorio grupal y control de commits |

---

## 🧱 Modelo de Datos

El sistema se basa en un modelo relacional que incluye entidades como:  
**Usuario, Rol, Reporte, Comentario, EstadoReporte, Categoría, ArchivoAdjunto, Área, Puntuación y Etiqueta**, con relaciones que permiten la trazabilidad y gestión completa de cada reporte.  

> 📊 *El diagrama entidad-relación se encuentra incluido en el repositorio para mayor detalle.*

---



## 📌 Lineamientos de Desarrollo

- Repositorio grupal en GitHub con commits semanales y mensajes descriptivos.  
- Documentación completa de APIs y componentes.  
- Validaciones, seguridad y manejo estructurado de errores.  
- Integración fluida entre servicios y consistencia de datos.  
- Dashboard interactivo y experiencia de usuario unificada.  

---

## 🚀 Próximos Pasos

- [ ] Definir responsabilidades individuales y tecnologías por integrante.  
- [ ] Implementar los servicios REST y GraphQL.  
- [ ] Desarrollar la capa de WebSockets en **Go** para notificaciones.  
- [ ] Crear e integrar el frontend con todas las capas.  
- [ ] Documentar endpoints, consultas y despliegue local.  

---

📂 **Repositorio oficial del proyecto:** *(https://github.com/jerenyvera09/trabajo_autonomoB-ser.git)*
