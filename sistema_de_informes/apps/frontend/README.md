# 🖥️ Frontend - Sistema de Reportes ULEAM

Frontend desarrollado con **React + TypeScript + Vite** para la **Semana 5** del proyecto.

Integra los tres servicios backend:

- ✅ **REST API** (Python/FastAPI)
- ✅ **GraphQL** (TypeScript/Apollo Server)
- ✅ **WebSocket** (Go/Gorilla)

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
- **Frontend**: React + TypeScript + Vite (Integración completa)

---

✅ **Frontend listo para evaluación - Semana 5 (Commit 3)**
{
files: ['**/*.{ts,tsx}'],
extends: [
// Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },

},
])

````

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
````
