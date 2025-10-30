# 🖥️ Frontend - Semana 6

**Responsable:** Equipo completo  
**Objetivo (Semana 6):** Completar funcionalidades CRUD, implementar autenticación, mejorar UI/UX con componentes reutilizables y agregar validaciones de formularios.

---

## ✅ Tareas completadas - Semana 6

### 1. Formularios y CRUD completo

**Crear Reportes:**

- Formulario con validación de campos obligatorios
- Campos: título, descripción, categoría, área, prioridad
- Integración con `POST /api/v1/reports` (REST API)
- Upload de archivos adjuntos (multipart/form-data)
- Notificación de éxito/error con toast

**Editar Reportes:**

- Formulario prellenado con datos del reporte
- Integración con `PUT /api/v1/reports/{id}`
- Validación de cambios antes de guardar

**Eliminar Reportes:**

- Modal de confirmación
- Integración con `DELETE /api/v1/reports/{id}`
- Actualización automática del listado

---

### 2. Autenticación implementada

**Login:**

- Formulario de autenticación (email + password)
- Integración con `POST /api/v1/auth/login` (REST API)
- Almacenamiento de JWT en `localStorage`
- Redirección automática tras login exitoso

**Protección de rutas:**

- Higher-Order Component (HOC) `withAuth`
- Redirección a `/login` si no hay token válido
- Header `Authorization: Bearer <token>` en todas las peticiones

**Logout:**

- Botón de cierre de sesión
- Limpieza de `localStorage`
- Redirección a `/login`

---

### 3. Componentes reutilizables

**Creados:**

- `<Button />` - Botón con variantes (primary, secondary, danger)
- `<Input />` - Input controlado con validación
- `<Select />` - Dropdown con opciones dinámicas
- `<Modal />` - Modal genérico para confirmaciones
- `<Card />` - Tarjeta de contenido reutilizable
- `<Spinner />` - Indicador de carga
- `<Toast />` - Notificaciones tipo toast

**Beneficios:**

- Código más mantenible
- Diseño consistente en toda la app
- Reducción de código duplicado

---

### 4. Filtros y búsqueda

**Implementados:**

- Búsqueda por texto (título/descripción)
- Filtro por estado (Abierto, En Proceso, Cerrado)
- Filtro por prioridad (Alta, Media, Baja)
- Filtro por categoría (consulta desde GraphQL)
- Filtro por área (consulta desde GraphQL)

**Debounce en búsqueda:**

- Optimización con `lodash.debounce` (300ms)
- Reducción de peticiones al backend

---

### 5. Paginación

- Listado de reportes con paginación (10 items por página)
- Botones Anterior/Siguiente
- Integración con `GET /api/v1/reports?limit=10&offset=0`
- Indicador de página actual y total de páginas

---

### 6. Mejoras de UI/UX

- **Loading states**: Spinners durante peticiones asíncronas
- **Error handling**: Mensajes de error amigables
- **Empty states**: Mensajes cuando no hay datos
- **Skeleton loaders**: Placeholders durante carga inicial
- **Animaciones**: Transiciones suaves con CSS transitions
- **Iconos**: Integración de `react-icons` para iconografía consistente

---

## 🧪 Pruebas realizadas

### Flujo de usuario completo:

1. **Login** → Ingresar credenciales → Obtener JWT
2. **Ver reportes** → Listado con paginación y filtros
3. **Crear reporte** → Formulario → POST REST → Notificación WebSocket → Recarga automática
4. **Editar reporte** → Modal → PUT REST → Actualización del listado
5. **Eliminar reporte** → Confirmación → DELETE REST → Actualización del listado
6. **Logout** → Limpieza de sesión → Redirección a login

**Resultado:** Flujo completo funcional sin errores.

---

## 🔧 Dependencias agregadas

```json
{
  "dependencies": {
    "@apollo/client": "^3.8.8",
    "graphql": "^16.8.1",
    "react-icons": "^4.12.0",
    "lodash.debounce": "^4.0.8"
  }
}
```

---

## 🔜 Próximos pasos (Semana 7)

- Tests E2E con Playwright o Cypress
- Optimización de rendimiento (React.memo, useMemo, useCallback)
- Documentación de componentes (Storybook o comentarios JSDoc)
- Build de producción y configuración de deploy
- Demo completa grabada en video

---

**Semana 6 completada — Frontend con CRUD completo, autenticación y UX profesional.**
