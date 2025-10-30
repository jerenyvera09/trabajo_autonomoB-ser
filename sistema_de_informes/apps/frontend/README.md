# 🖥️ Frontend - Semana 5

**Responsable:** Equipo completo (integración de todos los servicios)  
**Objetivo (Semana 5):** Desarrollar el frontend con React + TypeScript + Vite e integrar los tres servicios backend (REST, GraphQL, WebSocket).

---

## 🎯 Plan inicial - Semana 5

Integra los tres servicios backend:

- ✅ **REST API** (Python/FastAPI) - Puerto 8000
- ✅ **GraphQL** (TypeScript/Apollo Server) - Puerto 4000
- ✅ **WebSocket** (Go/Gorilla) - Puerto 8080

---

## ✅ Tareas completadas - Semana 5

1. **Setup del proyecto**:
   - Scaffolding con Vite + React + TypeScript
   - Configuración de ESLint y TypeScript strict mode
   - Estructura de carpetas: `src/components/`, `src/services/`, `src/hooks/`

2. **Integración con REST API**:
   - Cliente HTTP con `fetch` API
   - Endpoint: `GET /api/v1/reports`
   - Botón "Actualizar REST" para recargar datos
   - Renderizado de reportes en tarjetas (título, descripción, estado)

3. **Integración con GraphQL**:
   - Apollo Client configurado
   - Query GraphQL:
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
   - Botón "Actualizar GraphQL" para recargar datos

4. **Integración con WebSocket**:
   - Conexión automática a `ws://localhost:8080/ws`
   - Indicador visual del estado de conexión (verde/rojo)
   - Recepción de notificaciones en tiempo real
   - Banner de notificación animado
   - Recarga automática de datos al recibir evento `new_report`

5. **UI/UX implementada**:
   - Diseño responsivo (mobile-first)
   - Tema oscuro
   - Tarjetas de reportes con hover effects
   - Badges de estado con colores diferenciados (Abierto: verde, En Proceso: naranja, Cerrado: rojo)
   - Notificaciones animadas con auto-dismiss

---

## 📋 Requisitos previos

Antes de ejecutar el frontend, asegúrate de que los tres servicios estén corriendo:

1. **REST API** en `http://localhost:8000`
2. **GraphQL Server** en `http://localhost:4000`
3. **WebSocket Server** en `ws://localhost:8080/ws`

---

## 🚀 Instalación y ejecución

### 1. Instalar dependencias

```bash
cd sistema_de_informes/apps/frontend
npm install
```

### 2. Configurar variables de entorno (opcional)

Copia el archivo de ejemplo:

```bash
copy .env.example .env
```

Ajusta las URLs si es necesario (por defecto están configuradas correctamente).

### 3. Ejecutar en modo desarrollo

```bash
npm run dev
```

El frontend estará disponible en: **http://localhost:3000**

---

## 🎯 Funcionalidades implementadas

### ✅ Integración con REST API

- Consulta reportes desde `GET /api/v1/reports`
- Botón "Actualizar REST" para recargar datos
- Muestra reportes en tarjetas con título, descripción y estado

### ✅ Integración con GraphQL

- Consulta reportes mediante query GraphQL:
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
- Botón "Actualizar GraphQL" para recargar datos

### ✅ Integración con WebSocket

- Conexión automática a `ws://localhost:8080/ws`
- Indicador visual del estado de conexión
- Recibe notificaciones en tiempo real cuando se crea un nuevo reporte
- Banner de notificación que se muestra automáticamente
- Recarga automática de datos al recibir evento `new_report`

---

## 🧪 Probar la integración completa

### 1. Verificar que los servicios estén corriendo

**REST API:**

```bash
curl http://localhost:8000/health
```

**GraphQL:**
Abre http://localhost:4000/graphql en el navegador

**WebSocket:**

```bash
curl http://localhost:8080/
```

### 2. Simular notificación de nuevo reporte

Envía un mensaje al WebSocket para ver la notificación en el frontend:

```bash
curl -X POST http://localhost:8080/notify -H "Content-Type: application/json" -d "{\"message\":\"¡Nuevo reporte creado!\"}"
```

Deberías ver:

- ✅ Banner de notificación en la esquina superior derecha
- ✅ Recarga automática de los reportes
- ✅ Indicador de WebSocket en verde (conectado)

---

## 📦 Scripts disponibles

- `npm run dev` - Ejecutar en modo desarrollo (puerto 3000)
- `npm run build` - Compilar para producción
- `npm run preview` - Preview de la build de producción

---

## 🎨 Características de UI

- **Diseño responsivo** adaptado a diferentes tamaños de pantalla
- **Tema oscuro** para mejor experiencia visual
- **Tarjetas de reportes** con hover effects
- **Badges de estado** con colores diferenciados:
  - 🟢 Verde: Abierto
  - 🟠 Naranja: En Proceso
  - 🔴 Rojo: Cerrado
- **Notificaciones animadas** que se desvanecen automáticamente
- **Indicador de conexión WebSocket** en tiempo real

---

## 👥 Equipo de desarrollo

- **Integrante 1 (Cinthia Zambrano)**: REST API (Python/FastAPI)
- **Integrante 2 (Carlos Campuzano)**: GraphQL Server (TypeScript/Apollo)
- **Integrante 3 (Jereny Vera)**: WebSocket Server (Go/Gorilla)
- **Frontend**: Integración React + TypeScript + Vite (Equipo completo)

---

## 🔜 Próximos pasos (Semana 6)

- Agregar formularios para crear/editar reportes
- Implementar filtros y búsqueda
- Mejorar UI con componentes reutilizables
- Agregar paginación en listado de reportes
- Implementar autenticación con JWT

---

**Semana 5 completada — Frontend operativo con integración triple (REST + GraphQL + WebSocket).**`
