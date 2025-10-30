# 🚀 Servicio GraphQL - Sistema de Informes

Servicio GraphQL (Apollo Server v4 + TypeScript) que unifica entidades del sistema y expone queries analíticas. Compatible con el frontend gracias a alias en inglés.

## 🧭 Resumen rápido

- Puerto por defecto: http://localhost:4000
- Aliases para frontend: `reports`, `reportsAnalytics`, `categories`, `states`, `users`, `comments`, `ratings`, `files`, `tags`
- Las queries en español se mantienen (ej: `reportes`, `categorias`, `estados`)

## ▶️ Cómo iniciar (dev)

```powershell
cd sistema_de_informes\services\graphql
npm install
npm run dev
```

Playground: abre http://localhost:4000

## ⚙️ Configuración de REST desde GraphQL

Variables de entorno soportadas por el DataSource REST:

- REST_BASE_URL: URL base del REST (default http://localhost:8000)
- REST_API_TOKEN: Bearer opcional para endpoints protegidos

Fallbacks automáticos:

- /api/v1/<en> → si no existe, intenta su par en español (p. ej., /categorias, /estados-reporte, /usuarios, etc.)
- Adjuntos: /api/v1/attachments → /api/v1/files → /archivos

Con esto, GraphQL funciona sin tocar REST y, si defines REST_API_TOKEN, también leerá rutas protegidas.

## 📚 Esquema mínimo útil

```graphql
type KPI { clave: String!, valor: Int! }
type Report { id: ID!, title: String, status: String }
type ReportConnection { items: [Report!]!, total: Int!, limit: Int!, offset: Int! }
type ReportsAnalytics { total: Int!, byStatus: [KPI!]! }

type Query {
  reports(limit: Int = 50, offset: Int = 0): ReportConnection!
  reportsAnalytics: ReportsAnalytics!
}
```

---
Contenido histórico (extendido) a continuación:

**Semana 6**: Servidor GraphQL modular con **10 entidades**, **11 consultas analíticas** y **exportación compuesta con PDF real**.

> Compatibilidad con Frontend (alias): se añadieron alias en inglés para que el frontend actual funcione sin cambios.
>
> - reports: ReportConnection { items, total }
> - reportsAnalytics: { total, byStatus }
> - categories, states, users, comments, ratings, files, tags
> - Se mantienen las queries en español (reportes, categorias, estados, etc.).

---

## 📦 Estructura Modular## 📦 Estructura Modular## 📦 Estructura Modular

``````

src/

├── datasources/src/src/

│   └── rest.ts         # Cliente REST API unificado

├── resolvers/├── datasources/├── datasources/

│   ├── usuarios.ts     # Módulo 1: Autenticación

│   ├── roles.ts        # Módulo 1: Autenticación│   └── rest.ts         # Cliente REST API unificado│   └── rest.ts         # Cliente REST API unificado

│   ├── categorias.ts   # Módulo 2: Reportes

│   ├── areas.ts        # Módulo 2: Reportes├── resolvers/├── resolvers/

│   ├── estados.ts      # Módulo 2: Reportes

│   ├── reportes.ts     # Módulo 2: Reportes (principal)│   ├── usuarios.ts     # Módulo 1: Autenticación│   ├── usuarios.ts     # Módulo 1: Autenticación

│   ├── archivosAdjuntos.ts  # Módulo 2: Reportes

│   ├── comentarios.ts  # Módulo 3: Interacción│   ├── roles.ts        # Módulo 1: Autenticación│   ├── roles.ts        # Módulo 1: Autenticación

│   ├── puntuaciones.ts # Módulo 3: Interacción

│   ├── etiquetas.ts    # Módulo 3: Interacción│   ├── categorias.ts   # Módulo 2: Reportes│   ├── categorias.ts   # Módulo 2: Reportes

│   ├── analytics.ts    # Módulo 4: Analíticas (11 queries)

│   └── export.ts       # Módulo 5: PDF real con pdfkit│   ├── areas.ts        # Módulo 2: Reportes│   ├── areas.ts        # Módulo 2: Reportes

├── schema.ts           # Schema unificado

└── index.ts            # Servidor Apollo│   ├── estados.ts      # Módulo 2: Reportes│   ├── estados.ts      # Módulo 2: Reportes

```

│   ├── reportes.ts     # Módulo 2: Reportes (principal)│   ├── reportes.ts     # Módulo 2: Reportes (principal)

---

│   ├── archivosAdjuntos.ts  # Módulo 2: Reportes

## 🔌 Iniciar Servidor

│   ├── comentarios.ts  # Módulo 3: Interacción│   ├── archivosAdjuntos.ts  # Módulo 2: Reportes

```bash

cd sistema_de_informes\services\graphql│   ├── puntuaciones.ts # Módulo 3: Interacción

npm install

npm run dev│   ├── etiquetas.ts    # Módulo 3: Interacción│   ├── comentarios.ts  # Módulo 3: Interacción│   └── rest.ts         # Cliente REST API unificado

```

│   ├── analytics.ts    # Módulo 4: Analíticas (11 queries)

Servidor disponible en: **http://localhost:4000**

GraphQL Playground: **http://localhost:4000**│   └── export.ts       # Módulo 5: PDF real con pdfkit│   ├── puntuaciones.ts # Módulo 3: Interacción



---├── schema.ts           # Schema unificado



## 👥 Distribución de Queries Analíticas por Integrante└── index.ts            # Servidor Apollo│   ├── etiquetas.ts    # Módulo 3: Interacción├── resolvers/cmd



### **Integrante 1: Cinthia Zambrano (Python/FastAPI - REST)**```

1. `statsReportes` - Estadísticas generales de reportes (total, abiertos, cerrados, en proceso)

2. `reportesPorArea` - Filtrar reportes por área específica│   ├── analytics.ts    # Módulo 4: Analíticas (10 queries)

3. `topAreas` - Top N áreas con más reportes

---

## ⚙️ Configuración de REST desde GraphQL

Para consumir el servicio REST se usan variables de entorno y rutas con fallback:

- REST_BASE_URL: URL base del REST (default http://localhost:8000)
- REST_API_TOKEN: Token Bearer opcional para acceder a endpoints protegidos

Fallbacks automáticos en el DataSource:

- /api/v1/<en> → si no existe, intenta su par en español (p. ej., /categorias, /estados-reporte, /usuarios, etc.).
- Archivos adjuntos: intenta /api/v1/attachments → /api/v1/files → /archivos.

Esto permite que GraphQL funcione sin modificar el REST y, si se configura REST_API_TOKEN, también leer endpoints protegidos.

---

│   └── export.ts       # Módulo 5: PDF real con pdfkit│   ├── usuarios.ts     # Módulo 1: Autenticacióncd sistema_de_informes\services\graphql

### **Integrante 2: Carlos Campuzano (TypeScript/Apollo - GraphQL)**

1. `reportesPorCategoria` - Filtrar reportes por categoría## 🔌 Iniciar Servidor

2. `promedioPuntuaciones` - Calcular promedio de todas las puntuaciones

3. `etiquetasMasUsadas` - Top N etiquetas más frecuentes├── schema.ts           # Schema unificado



---```bash



### **Integrante 3: Jereny Vera (Go/Gorilla - WebSocket)**cd sistema_de_informes\services\graphql└── index.ts            # Servidor Apollo│   ├── roles.ts        # Módulo 1: Autenticaciónnpm install

1. `reportesPorUsuario` - Reportes creados por un usuario específico

2. `actividadReciente` - Actividad mezclada (reportes + comentarios ordenados por fecha)npm install

3. `usuariosMasActivos` - Top N usuarios con más reportes creados

4. `reportAnalytics` ⭐ - Query compuesto que agrega datos de múltiples entidades y genera PDF descargablenpm run dev```



---```



### **Queries Adicionales (Equipo)**│ ├── categorias.ts # Módulo 2: Reportes

1. `reportesPorEstado` - Filtrar reportes por estado específico

2. `reportesPorFecha` - Filtrar reportes en un rango de fechasServidor disponible en: **http://localhost:4000**



---GraphQL Playground: **http://localhost:4000**---



## 📊 Queries Disponibles



### **Módulo 1: Autenticación**---│ ├── areas.ts # Módulo 2: Reportes



| Query | Descripción | Parámetros | Ejemplo |

|-------|-------------|------------|---------|

| `usuarios` | Lista todos los usuarios | - | `{ usuarios { id name email } }` |## 📊 Queries Disponibles## 🔌 Iniciar Servidor

| `usuario(id)` | Busca usuario por ID | `id: ID!` | `{ usuario(id: "1") { name email } }` |

| `usuariosByStatus` | Filtra por status | `status: String!` | `{ usuariosByStatus(status: "active") { name } }` |

| `roles` | Lista todos los roles | - | `{ roles { id name } }` |

| `rol(id)` | Busca rol por ID | `id: ID!` | `{ rol(id: "1") { name } }` |### **Módulo 1: Autenticación**│ ├── estados.ts # Módulo 2: Reportes## Ejecutar en desarrollo



---



### **Módulo 2: Reportes**| Query | Descripción | Parámetros | Ejemplo |````bash



| Query | Descripción | Parámetros | Ejemplo ||-------|-------------|------------|---------|

|-------|-------------|------------|---------|

| `reportes` | Lista todos los reportes | - | `{ reportes { id title status } }` || `usuarios` | Lista todos los usuarios | - | `{ usuarios { id name email } }` |npm install│   ├── reportes.ts     # Módulo 2: Reportes (entidad principal)

| `reporte(id)` | Busca reporte por ID | `id: ID!` | `{ reporte(id: "1") { title description } }` |

| `reportesByStatus` | Filtra por estado | `status: String!` | `{ reportesByStatus(status: "Abierto") { title } }` || `usuario(id)` | Busca usuario por ID | `id: ID!` | `{ usuario(id: "1") { name email } }` |

| `reportesByPriority` | Filtra por prioridad | `priority: String!` | `{ reportesByPriority(priority: "Alta") { title } }` |

| `categorias` | Lista categorías | - | `{ categorias { id name } }` || `usuariosByStatus` | Filtra por status | `status: String!` | `{ usuariosByStatus(status: "active") { name } }` |npm run dev

| `categoria(id)` | Busca categoría | `id: ID!` | `{ categoria(id: "1") { name } }` |

| `categoriasByPriority` | Filtra por prioridad | `priority: String!` | `{ categoriasByPriority(priority: "Alta") { name } }` || `roles` | Lista todos los roles | - | `{ roles { id name } }` |

| `areas` | Lista áreas | - | `{ areas { id name } }` |

| `area(id)` | Busca área | `id: ID!` | `{ area(id: "1") { name } }` || `rol(id)` | Busca rol por ID | `id: ID!` | `{ rol(id: "1") { name } }` |```│   ├── archivosAdjuntos.ts  # Módulo 2: Reportescmd

| `areasByResponsable` | Filtra por responsable | `responsable: String!` | `{ areasByResponsable(responsable: "Juan") { name } }` |

| `estados` | Lista estados | - | `{ estados { id name } }` |

| `estado(id)` | Busca estado | `id: ID!` | `{ estado(id: "1") { name } }` |

| `estadosFinal` | Estados finales | `isFinal: Boolean!` | `{ estadosFinal(isFinal: true) { name } }` |---

| `archivosAdjuntos` | Lista archivos | - | `{ archivosAdjuntos { id filename url } }` |

| `archivoAdjunto(id)` | Busca archivo | `id: ID!` | `{ archivoAdjunto(id: "1") { filename } }` |

| `archivosByReporte` | Archivos de reporte | `reporteId: ID!` | `{ archivosByReporte(reporteId: "1") { filename } }` |

### **Módulo 2: Reportes**Servidor disponible en: **http://localhost:4000**  │   ├── comentarios.ts  # Módulo 3: Interacciónnpm run dev

---



### **Módulo 3: Interacción**

| Query | Descripción | Parámetros | Ejemplo |GraphQL Playground: **http://localhost:4000**

| Query | Descripción | Parámetros | Ejemplo |

|-------|-------------|------------|---------||-------|-------------|------------|---------|

| `comentarios` | Lista comentarios | - | `{ comentarios { id content } }` |

| `comentario(id)` | Busca comentario | `id: ID!` | `{ comentario(id: "1") { content } }` || `reportes` | Lista todos los reportes | - | `{ reportes { id title status } }` |│   ├── puntuaciones.ts # Módulo 3: Interacción

| `comentariosByReporte` | Comentarios de reporte | `reporteId: ID!` | `{ comentariosByReporte(reporteId: "1") { content } }` |

| `comentariosByUsuario` | Comentarios de usuario | `usuarioId: ID!` | `{ comentariosByUsuario(usuarioId: "1") { content } }` || `reporte(id)` | Busca reporte por ID | `id: ID!` | `{ reporte(id: "1") { title description } }` |

| `puntuaciones` | Lista puntuaciones | - | `{ puntuaciones { id value } }` |

| `puntuacion(id)` | Busca puntuación | `id: ID!` | `{ puntuacion(id: "1") { value } }` || `reportesByStatus` | Filtra por estado | `status: String!` | `{ reportesByStatus(status: "Abierto") { title } }` |---

| `puntuacionesByReporte` | Puntuaciones de reporte | `reporteId: ID!` | `{ puntuacionesByReporte(reporteId: "1") { value } }` |

| `etiquetas` | Lista etiquetas | - | `{ etiquetas { id name } }` || `reportesByPriority` | Filtra por prioridad | `priority: String!` | `{ reportesByPriority(priority: "Alta") { title } }` |

| `etiqueta(id)` | Busca etiqueta | `id: ID!` | `{ etiqueta(id: "1") { name } }` |

| `categorias` | Lista categorías | - | `{ categorias { id name } }` |│   ├── etiquetas.ts    # Módulo 3: Interacción

---

| `categoria(id)` | Busca categoría | `id: ID!` | `{ categoria(id: "1") { name } }` |

### **Módulo 4: Analíticas (11 Queries Compuestas)**

| `categoriasByPriority` | Filtra por prioridad | `priority: String!` | `{ categoriasByPriority(priority: "Alta") { name } }` |## 👥 Distribución de Queries Analíticas por Integrante

| # | Query | Descripción | Responsable | Parámetros | Ejemplo |

|---|-------|-------------|-------------|------------|---------|| `areas` | Lista áreas | - | `{ areas { id name } }` |

| 1️⃣ | `statsReportes` | Estadísticas generales | **Cinthia Zambrano** | - | `{ statsReportes { total abiertos cerrados } }` |

| 2️⃣ | `reportesPorArea` | Reportes por área | **Cinthia Zambrano** | `area: String!` | `{ reportesPorArea(area: "TI") { title } }` || `area(id)` | Busca área | `id: ID!` | `{ area(id: "1") { name } }` |│   ├── analytics.ts    # Módulo 4: Analíticas (10 queries)Salida esperada:

| 3️⃣ | `reportesPorCategoria` | Reportes por categoría | **Carlos Campuzano** | `categoria: String!` | `{ reportesPorCategoria(categoria: "Bug") { title } }` |

| 4️⃣ | `reportesPorEstado` | Reportes filtrados por estado | **Equipo** | `estado: String!` | `{ reportesPorEstado(estado: "Abierto") { title } }` || `areasByResponsable` | Filtra por responsable | `responsable: String!` | `{ areasByResponsable(responsable: "Juan") { name } }` |

| 5️⃣ | `reportesPorUsuario` | Reportes de usuario | **Jereny Vera** | `usuario: ID!` | `{ reportesPorUsuario(usuario: "1") { title } }` |

| 6️⃣ | `actividadReciente` | Actividad mezclada | **Jereny Vera** | `limit: Int` | `{ actividadReciente(limit: 5) }` || `estados` | Lista estados | - | `{ estados { id name } }` |### **Integrante 1: [Nombre Completo]**

| 7️⃣ | `topAreas` | Top áreas con reportes | **Cinthia Zambrano** | `limit: Int` | `{ topAreas(limit: 3) { area cantidad } }` |

| 8️⃣ | `promedioPuntuaciones` | Promedio de ratings | **Carlos Campuzano** | - | `{ promedioPuntuaciones }` || `estado(id)` | Busca estado | `id: ID!` | `{ estado(id: "1") { name } }` |

| 9️⃣ | `etiquetasMasUsadas` | Etiquetas más frecuentes | **Carlos Campuzano** | `limit: Int` | `{ etiquetasMasUsadas(limit: 5) { clave valor } }` |

| 🔟 | `reportesPorFecha` | Reportes en rango | **Equipo** | `desde: String!`, `hasta: String!` | `{ reportesPorFecha(desde: "2024-01-01", hasta: "2024-12-31") { title } }` || `estadosFinal` | Estados finales | `isFinal: Boolean!` | `{ estadosFinal(isFinal: true) { name } }` |1. **statsReportes**: Estadísticas generales (total, abiertos, cerrados, en proceso)│   └── export.ts       # Módulo 5: Exportación (reportAnalytics)

| 1️⃣1️⃣ | `usuariosMasActivos` | Usuarios con más reportes | **Jereny Vera** | `limit: Int` | `{ usuariosMasActivos(limit: 3) { clave valor } }` |

| `archivosAdjuntos` | Lista archivos | - | `{ archivosAdjuntos { id filename url } }` |

---

| `archivoAdjunto(id)` | Busca archivo | `id: ID!` | `{ archivoAdjunto(id: "1") { filename } }` |2. **reportesPorArea**: Filtrar reportes por área específica

### **Módulo 5: Exportación Compuesta (PDF Real)** ⭐

| `archivosByReporte` | Archivos de reporte | `reporteId: ID!` | `{ archivosByReporte(reporteId: "1") { filename } }` |

| Query | Descripción | Responsable | Parámetros | Ejemplo |

|-------|-------------|-------------|------------|---------|3. **topAreas**: Top N áreas con más reportes├── schema.ts           # Schema unificado

| `reportAnalytics` | **Reporte completo con PDF descargable** | **Jereny Vera** | `reporteId: ID!`, `formato: String` | Ver ejemplo abajo ⬇️ |

---

**Características:**

- Agrega datos de 7 entidades REST: `reporte` + `comentarios` + `puntuaciones` + `archivos` + `usuario` + `categoría` + `estado`

- Genera PDF real con `pdfkit` en formato base64

- Exporta como JSON (default) o PDF (`formato="pdf"`)### **Módulo 3: Interacción**



#### Ejemplo de `reportAnalytics`:### **Integrante 2: [Nombre Completo]**└── index.ts            # Servidor Apollo🚀 Servidor GraphQL listo en http://localhost:4000/



```graphql| Query | Descripción | Parámetros | Ejemplo |

{

  reportAnalytics(reporteId: "1", formato: "pdf") {|-------|-------------|------------|---------|1. **reportesPorCategoria**: Filtrar reportes por categoría

    reporte {

      id| `comentarios` | Lista comentarios | - | `{ comentarios { id content } }` |

      title

      description| `comentario(id)` | Busca comentario | `id: ID!` | `{ comentario(id: "1") { content } }` |2. **promedioPuntuaciones**: Calcular promedio de todas las puntuaciones```

      status

      priority| `comentariosByReporte` | Comentarios de reporte | `reporteId: ID!` | `{ comentariosByReporte(reporteId: "1") { content } }` |

    }

    comentarios {| `comentariosByUsuario` | Comentarios de usuario | `usuarioId: ID!` | `{ comentariosByUsuario(usuarioId: "1") { content } }` |3. **etiquetasMasUsadas**: Top N etiquetas más frecuentes

      id

      content| `puntuaciones` | Lista puntuaciones | - | `{ puntuaciones { id value } }` |

      date

    }| `puntuacion(id)` | Busca puntuación | `id: ID!` | `{ puntuacion(id: "1") { value } }` |---El playground de GraphQL estará disponible en: _http://localhost:4000/graphql_

    puntuaciones {

      id| `puntuacionesByReporte` | Puntuaciones de reporte | `reporteId: ID!` | `{ puntuacionesByReporte(reporteId: "1") { value } }` |

      value

    }| `etiquetas` | Lista etiquetas | - | `{ etiquetas { id name } }` |### **Integrante 3: Jereny Vera**

    archivos {

      id| `etiqueta(id)` | Busca etiqueta | `id: ID!` | `{ etiqueta(id: "1") { name } }` |

      filename

      url1. **reportesPorUsuario**: Reportes creados por un usuario específico## 🔌 Iniciar Servidor---

    }

    usuario {---

      id

      name2. **actividadReciente**: Actividad mezclada (reportes + comentarios ordenados)

      email

    }### **Módulo 4: Analíticas (11 Queries Compuestas)**

    categoria {

      id3. **usuariosMasActivos**: Top N usuarios con más reportes creados```bash## 🔗 Integración con REST (Semana 5)

      name

    }| # | Query | Descripción | Parámetros | Ejemplo |

    estado {

      id|---|-------|-------------|------------|---------|4. **reportAnalytics** ⭐: Query compuesto que agrega datos de múltiples entidades y genera PDF descargable

      name

    }| 1️⃣ | `statsReportes` | Estadísticas generales | - | `{ statsReportes { total abiertos cerrados } }` |

    formato

    pdfBase64  # PDF real en base64 (descargable)| 2️⃣ | `reportesPorArea` | Reportes por área | `area: String!` | `{ reportesPorArea(area: "TI") { title } }` |npm install

  }

}| 3️⃣ | `reportesPorCategoria` | Reportes por categoría | `categoria: String!` | `{ reportesPorCategoria(categoria: "Bug") { title } }` |

```

| 4️⃣ | `reportesPorEstado` | Reportes filtrados por estado | `estado: String!` | `{ reportesPorEstado(estado: "Abierto") { title } }` |### **Queries Adicionales (Equipo)**

#### Descargar PDF desde el navegador:

| 5️⃣ | `reportesPorUsuario` | Reportes de usuario | `usuario: ID!` | `{ reportesPorUsuario(usuario: "1") { title } }` |

```javascript

// Ejecutar en consola del navegador después del query| 6️⃣ | `actividadReciente` | Actividad mezclada | `limit: Int` | `{ actividadReciente(limit: 5) }` |1. **reportesPorFecha**: Filtrar reportes en rango de fechasnpm run devEl resolver reports consume el endpoint del servicio REST:

const base64 = data.reportAnalytics.pdfBase64;

const link = document.createElement('a');| 7️⃣ | `topAreas` | Top áreas con reportes | `limit: Int` | `{ topAreas(limit: 3) { area cantidad } }` |

link.href = 'data:application/pdf;base64,' + base64;

link.download = 'reporte_analytics.pdf';| 8️⃣ | `promedioPuntuaciones` | Promedio de ratings | - | `{ promedioPuntuaciones }` |

link.click();

```| 9️⃣ | `etiquetasMasUsadas` | Etiquetas más frecuentes | `limit: Int` | `{ etiquetasMasUsadas(limit: 5) { clave valor } }` |



---| 🔟 | `reportesPorFecha` | Reportes en rango | `desde: String!`, `hasta: String!` | `{ reportesPorFecha(desde: "2024-01-01", hasta: "2024-12-31") { title } }` |---```



## 🔗 Integración con REST API| 1️⃣1️⃣ | `usuariosMasActivos` | Usuarios con más reportes | `limit: Int` | `{ usuariosMasActivos(limit: 3) { clave valor } }` |



Todas las queries consumen el REST API (`http://localhost:8000`) mediante el datasource centralizado:



**Archivo:** `src/datasources/rest.ts`---



```typescript## 📊 Queries Disponiblesgraphql

import { restAPI } from "../datasources/rest.js";

### **Módulo 5: Exportación Compuesta (PDF Real)** ⭐

// Ejemplo: Obtener reportes desde REST

const reports = await restAPI.getReports();

```

| Query | Descripción | Parámetros | Ejemplo |

**Requisito:** El servicio REST debe estar ejecutándose antes de hacer consultas GraphQL.

|-------|-------------|------------|---------|### **Módulo 1: Autenticación**Servidor disponible en: **http://localhost:4000** query GetReports {

---

| `reportAnalytics` | **Reporte completo con PDF descargable** | `reporteId: ID!`, `formato: String` | Ver ejemplo abajo ⬇️ |

## 🔗 Integración con WebSocket



El REST API notifica automáticamente al WebSocket cuando ocurren eventos:

**Características:**

| Evento | Trigger | Endpoint REST | Notificación WS |

|--------|---------|---------------|-----------------|- Agrega datos de 7 entidades REST: `reporte` + `comentarios` + `puntuaciones` + `archivos` + `usuario` + `categoría` + `estado`| Query | Descripción | Parámetros | Ejemplo |GraphQL Playground: **http://localhost:4000** reports {

| `new_report` | Crear reporte | `POST /reportes` | `notify_new_report()` |

| `update_report` | Actualizar reporte | `PUT /reportes/{id}` | `notify_update_report()` |- Genera PDF real con `pdfkit` en formato base64

| `comment_added` | Agregar comentario | `POST /comentarios` | `notify_comment_added()` |

- Exporta como JSON (default) o PDF (`formato="pdf"`)|-------|-------------|------------|---------|

Los clientes conectados al WebSocket (`ws://localhost:8080/ws?room=reports`) reciben las notificaciones en tiempo real.



---

#### Ejemplo de `reportAnalytics`:| `usuarios` | Lista todos los usuarios | - | `{ usuarios { id name email } }` |    id

## 🛠️ Tecnologías



- **Apollo Server** 4.x

- **TypeScript** con ES Modules```graphql| `usuario(id)` | Busca usuario por ID | `id: ID!` | `{ usuario(id: "1") { name email } }` |

- **Fetch API** para consultas REST

- **pdfkit** para generación real de PDFs{

- **Patrón Datasource** para centralizar lógica REST

  reportAnalytics(reporteId: "1", formato: "pdf") {| `usuariosByStatus` | Filtra por status | `status: String!` | `{ usuariosByStatus(status: "active") { name } }` |--- title

---

    reporte {

## 📝 Notas Importantes

      id| `roles` | Lista todos los roles | - | `{ roles { id name } }` |

- ✅ Todas las queries consumen el **REST API** (`http://localhost:8000`)

- ✅ Sin mutaciones (GraphQL es **solo lectura**)      title

- ✅ Modular: cada entidad en archivo separado

- ✅ **11 queries analíticas** (3 por integrante + 2 del equipo)      description| `rol(id)` | Busca rol por ID | `id: ID!` | `{ rol(id: "1") { name } }` |    description

- ✅ Query compuesto `reportAnalytics` con **PDF REAL** descargable

- ✅ **REST API notifica automáticamente al WebSocket** cuando se crea/actualiza un reporte o comentario      status

- ✅ **Frontend consume queries analíticas** en dashboard interactivo

      priority

---

    }

## 🧪 Probar Queries

    comentarios {---## 📊 Queries Disponibles status

Abre **http://localhost:4000** en el navegador y ejecuta:

      id

```graphql

# 1. Estadísticas generales (Integrante 1)      content

{

  statsReportes {      date

    total

    abiertos    }### **Módulo 2: Reportes**    priority

    cerrados

    enProceso    puntuaciones {

  }

}      id



# 2. Top áreas con reportes (Integrante 1)      value

{

  topAreas(limit: 3) {    }| Query | Descripción | Parámetros | Ejemplo |### **Módulo 1: Autenticación** }

    area

    cantidad    archivos {

  }

}      id|-------|-------------|------------|---------|



# 3. Promedio de puntuaciones (Integrante 2)      filename

{

  promedioPuntuaciones      url| `reportes` | Lista todos los reportes | - | `{ reportes { id title status } }` |}

}

    }

# 4. Usuarios más activos (Integrante 3)

{    usuario {| `reporte(id)` | Busca reporte por ID | `id: ID!` | `{ reporte(id: "1") { title description } }` |

  usuariosMasActivos(limit: 5) {

    clave      id

    valor

  }      name| `reportesByStatus` | Filtra por estado | `status: String!` | `{ reportesByStatus(status: "Abierto") { title } }` || Query | Descripción | Parámetros | Ejemplo |

}

      email

# 5. Reportes filtrados por estado (Equipo)

{    }| `reportesByPriority` | Filtra por prioridad | `priority: String!` | `{ reportesByPriority(priority: "Alta") { title } }` |

  reportesPorEstado(estado: "Abierto") {

    id    categoria {

    title

    status      id| `categorias` | Lista categorías | - | `{ categorias { id name } }` ||-------|-------------|------------|---------|

  }

}      name



# 6. Analytics completo con PDF (Integrante 3)    }| `categoria(id)` | Busca categoría | `id: ID!` | `{ categoria(id: "1") { name } }` |

{

  reportAnalytics(reporteId: "1", formato: "pdf") {    estado {

    reporte { title status }

    comentarios { content }      id| `categoriasByPriority` | Filtra por prioridad | `priority: String!` | `{ categoriasByPriority(priority: "Alta") { name } }` || `usuarios` | Lista todos los usuarios | - | `{ usuarios { id name email } }` |Este query realiza internamente:

    usuario { name }

    pdfBase64      name

  }

}    }| `areas` | Lista áreas | - | `{ areas { id name } }` |

```

    formato

---

    pdfBase64  # PDF real en base64 (descargable)| `area(id)` | Busca área | `id: ID!` | `{ area(id: "1") { name } }` || `usuario(id)` | Busca usuario por ID | `id: ID!` | `{ usuario(id: "1") { name email } }` |

**Semana 6** - Sistema de Informes Universidad 🚀

**Cumplimiento 100%** con requisitos del docente ✅  }


}| `areasByResponsable` | Filtra por responsable | `responsable: String!` | `{ areasByResponsable(responsable: "Juan") { name } }` |

```

| `estados` | Lista estados | - | `{ estados { id name } }` || `usuariosByStatus` | Filtra por status | `status: String!` | `{ usuariosByStatus(status: "active") { name } }` |

#### Descargar PDF desde el navegador:

| `estado(id)` | Busca estado | `id: ID!` | `{ estado(id: "1") { name } }` |

```javascript

// Ejecutar en consola del navegador después del query| `estadosFinal` | Estados finales | `isFinal: Boolean!` | `{ estadosFinal(isFinal: true) { name } }` || `roles` | Lista todos los roles | - | `{ roles { id name } }` |GET http://localhost:8000/api/v1/reports

const base64 = data.reportAnalytics.pdfBase64;

const link = document.createElement('a');| `archivosAdjuntos` | Lista archivos | - | `{ archivosAdjuntos { id filename url } }` |

link.href = 'data:application/pdf;base64,' + base64;

link.download = 'reporte_analytics.pdf';| `archivoAdjunto(id)` | Busca archivo | `id: ID!` | `{ archivoAdjunto(id: "1") { filename } }` || `rol(id)` | Busca rol por ID | `id: ID!` | `{ rol(id: "1") { name } }` |

link.click();

```| `archivosByReporte` | Archivos de reporte | `reporteId: ID!` | `{ archivosByReporte(reporteId: "1") { filename } }` |



------_Requisito_: El servicio REST debe estar ejecutándose antes de hacer esta consulta.



## 🔗 Integración con REST API---



Todas las queries consumen el REST API (`http://localhost:8000`) mediante el datasource centralizado:### **Módulo 2: Reportes**---



**Archivo:** `src/datasources/rest.ts`### **Módulo 3: Interacción**



```typescript| Query | Descripción | Parámetros | Ejemplo |## Pruebas rápidas (GraphQL)

import { restAPI } from "../datasources/rest.js";

| Query | Descripción | Parámetros | Ejemplo |

// Ejemplo: Obtener reportes desde REST

const reports = await restAPI.getReports();|-------|-------------|------------|---------||-------|-------------|------------|---------|

```

| `comentarios` | Lista comentarios | - | `{ comentarios { id content } }` |

**Requisito:** El servicio REST debe estar ejecutándose antes de hacer consultas GraphQL.

| `comentario(id)` | Busca comentario | `id: ID!` | `{ comentario(id: "1") { content } }` || `reportes` | Lista todos los reportes | - | `{ reportes { id title status } }` |### 1. Query de reportes desde REST API:

---

| `comentariosByReporte` | Comentarios de reporte | `reporteId: ID!` | `{ comentariosByReporte(reporteId: "1") { content } }` |

## 🔗 Integración con WebSocket

| `comentariosByUsuario` | Comentarios de usuario | `usuarioId: ID!` | `{ comentariosByUsuario(usuarioId: "1") { content } }` || `reporte(id)` | Busca reporte por ID | `id: ID!` | `{ reporte(id: "1") { title description } }` |

El REST API notifica automáticamente al WebSocket cuando ocurren eventos:

| `puntuaciones` | Lista puntuaciones | - | `{ puntuaciones { id value } }` |

| Evento | Trigger | Endpoint REST | Notificación WS |

|--------|---------|---------------|-----------------|| `puntuacion(id)` | Busca puntuación | `id: ID!` | `{ puntuacion(id: "1") { value } }` || `reportesByStatus` | Filtra por estado | `status: String!` | `{ reportesByStatus(status: "Abierto") { title } }` |graphql

| `new_report` | Crear reporte | `POST /reportes` | `notify_new_report()` |

| `update_report` | Actualizar reporte | `PUT /reportes/{id}` | `notify_update_report()` || `puntuacionesByReporte` | Puntuaciones de reporte | `reporteId: ID!` | `{ puntuacionesByReporte(reporteId: "1") { value } }` |

| `comment_added` | Agregar comentario | `POST /comentarios` | `notify_comment_added()` |

| `etiquetas` | Lista etiquetas | - | `{ etiquetas { id name } }` || `reportesByPriority` | Filtra por prioridad | `priority: String!` | `{ reportesByPriority(priority: "Alta") { title } }` |query {

Los clientes conectados al WebSocket (`ws://localhost:8080/ws?room=reports`) reciben las notificaciones en tiempo real.

| `etiqueta(id)` | Busca etiqueta | `id: ID!` | `{ etiqueta(id: "1") { name } }` |

---

| `categorias` | Lista categorías | - | `{ categorias { id name } }` | reports {

## 🛠️ Tecnologías

---

- **Apollo Server** 4.x

- **TypeScript** con ES Modules| `categoria(id)` | Busca categoría | `id: ID!` | `{ categoria(id: "1") { name } }` | id

- **Fetch API** para consultas REST

- **pdfkit** para generación real de PDFs### **Módulo 4: Analíticas (10 Queries)**

- **Patrón Datasource** para centralizar lógica REST

| `categoriasByPriority` | Filtra por prioridad | `priority: String!` | `{ categoriasByPriority(priority: "Alta") { name } }` | title

---

| # | Query | Descripción | Integrante | Ejemplo |

## 📝 Notas Importantes

|---|-------|-------------|------------|---------|| `areas` | Lista áreas | - | `{ areas { id name } }` | description

- ✅ Todas las queries consumen el **REST API** (`http://localhost:8000`)

- ✅ Sin mutaciones (GraphQL es **solo lectura**)| 1️⃣ | `statsReportes` | Estadísticas generales | **Integrante 1** | `{ statsReportes { total abiertos cerrados } }` |

- ✅ Modular: cada entidad en archivo separado

- ✅ **11 queries analíticas** combinando múltiples entidades| 2️⃣ | `reportesPorArea` | Reportes por área | **Integrante 1** | `{ reportesPorArea(area: "TI") { title } }` || `area(id)` | Busca área | `id: ID!` | `{ area(id: "1") { name } }` | status

- ✅ Query compuesto `reportAnalytics` con **PDF REAL** descargable

- ✅ **REST API notifica automáticamente al WebSocket** cuando se crea/actualiza un reporte o comentario| 3️⃣ | `topAreas` | Top áreas con reportes | **Integrante 1** | `{ topAreas(limit: 3) { area cantidad } }` |



---| 4️⃣ | `reportesPorCategoria` | Reportes por categoría | **Integrante 2** | `{ reportesPorCategoria(categoria: "Bug") { title } }` || `areasByResponsable` | Filtra por responsable | `responsable: String!` | `{ areasByResponsable(responsable: "Juan") { name } }` | priority



## 🧪 Probar Queries| 5️⃣ | `promedioPuntuaciones` | Promedio de ratings | **Integrante 2** | `{ promedioPuntuaciones }` |



Abre **http://localhost:4000** en el navegador y ejecuta:| 6️⃣ | `etiquetasMasUsadas` | Etiquetas más frecuentes | **Integrante 2** | `{ etiquetasMasUsadas(limit: 5) { clave valor } }` || `estados` | Lista estados | - | `{ estados { id name } }` | }



```graphql| 7️⃣ | `reportesPorUsuario` | Reportes de usuario | **Integrante 3** | `{ reportesPorUsuario(usuario: "1") { title } }` |

# 1. Estadísticas generales

{| 8️⃣ | `actividadReciente` | Actividad mezclada | **Integrante 3** | `{ actividadReciente(limit: 5) }` || `estado(id)` | Busca estado | `id: ID!` | `{ estado(id: "1") { name } }` |}

  statsReportes {

    total| 9️⃣ | `usuariosMasActivos` | Usuarios con más reportes | **Integrante 3** | `{ usuariosMasActivos(limit: 3) { clave valor } }` |

    abiertos

    cerrados| 🔟 | `reportesPorFecha` | Reportes en rango | **Equipo** | `{ reportesPorFecha(desde: "2024-01-01", hasta: "2024-12-31") { title } }` || `estadosFinal` | Estados finales | `isFinal: Boolean!` | `{ estadosFinal(isFinal: true) { name } }` |

    enProceso

  }

}

---| `archivosAdjuntos` | Lista archivos | - | `{ archivosAdjuntos { id filename url } }` |

# 2. Reportes filtrados por estado (nuevo query agregado)

{

  reportesPorEstado(estado: "Abierto") {

    id### **Módulo 5: Exportación Compuesta (PDF Real)** ⭐| `archivoAdjunto(id)` | Busca archivo | `id: ID!` | `{ archivoAdjunto(id: "1") { filename } }` |### 2. Query lista de reportes (mock local):

    title

    status

  }

}| Query | Descripción | Integrante | Características || `archivosByReporte` | Archivos de reporte | `reporteId: ID!` | `{ archivosByReporte(reporteId: "1") { filename } }` |



# 3. Analytics completo con PDF|-------|-------------|------------|-----------------|

{

  reportAnalytics(reporteId: "1", formato: "pdf") {| `reportAnalytics` | **Reporte completo con PDF descargable** | **Integrante 3** | Agrega datos de múltiples entidades (reporte + comentarios + puntuaciones + archivos + usuario + categoría + estado). Genera PDF real con `pdfkit` en formato base64. |`graphql

    reporte { title status }

    comentarios { content }

    usuario { name }

    pdfBase64#### Ejemplo de `reportAnalytics`:---

  }

}

```

```graphqlgraphql

---

{

**Semana 6** - Sistema de Informes Universidad 🚀

**Cumplimiento 100%** con requisitos del docente ✅  reportAnalytics(reporteId: "1", formato: "pdf") {### **Módulo 3: Interacción**query {


    reporte {

      idreportes {

      title

      description| Query | Descripción | Parámetros | Ejemplo | id

      status

      priority|-------|-------------|------------|---------| titulo

    }

    comentarios {| `comentarios` | Lista comentarios | - | `{ comentarios { id content } }` | estado

      id

      content| `comentario(id)` | Busca comentario | `id: ID!` | `{ comentario(id: "1") { content } }` | categoria

      date

    }| `comentariosByReporte` | Comentarios de reporte | `reporteId: ID!` | `{ comentariosByReporte(reporteId: "1") { content } }` | creadoEn

    puntuaciones {

      id| `comentariosByUsuario` | Comentarios de usuario | `usuarioId: ID!` | `{ comentariosByUsuario(usuarioId: "1") { content } }` | }

      value

    }| `puntuaciones` | Lista puntuaciones | - | `{ puntuaciones { id value } }` |}

    archivos {

      id| `puntuacion(id)` | Busca puntuación | `id: ID!` | `{ puntuacion(id: "1") { value } }` |`

      filename

      url| `puntuacionesByReporte` | Puntuaciones de reporte | `reporteId: ID!` | `{ puntuacionesByReporte(reporteId: "1") { value } }` |

    }

    usuario {| `etiquetas` | Lista etiquetas | - | `{ etiquetas { id name } }` |- Crear reporte:

      id

      name| `etiqueta(id)` | Busca etiqueta | `id: ID!` | `{ etiqueta(id: "1") { name } }` |

      email

    }graphql

    categoria {

      id---mutation {

      name

    }crearReporte(input: { titulo: "Nueva incidencia", descripcion: "Detalle" }) {

    estado {

      id### **Módulo 4: Analíticas (10 Queries)** id

      name

    }    titulo

    formato

    pdfBase64  # PDF real en base64 (descargable)| # | Query | Descripción | Parámetros | Ejemplo | estado

  }

}|---|-------|-------------|------------|---------| }

````

| 1️⃣ | `statsReportes` | Estadísticas generales | - | `{ statsReportes { total abiertos cerrados } }` |}

#### Descargar PDF desde el navegador:

| 2️⃣ | `reportesPorArea` | Reportes por área | `area: String!` | `{ reportesPorArea(area: "TI") { title } }` |```

````javascript

// Ejecutar en consola del navegador después del query| 3️⃣ | `reportesPorCategoria` | Reportes por categoría | `categoria: String!` | `{ reportesPorCategoria(categoria: "Bug") { title } }` |> Nota: En Semana 4 los datos están en memoria (mock). En Semanas 5-6 se integrará con el REST/DB.

const base64 = data.reportAnalytics.pdfBase64;| 4️⃣ | `reportesPorUsuario` | Reportes de usuario | `usuario: ID!` | `{ reportesPorUsuario(usuario: "1") { title } }` |

const link = document.createElement('a');| 5️⃣ | `actividadReciente` | Actividad mezclada | `limit: Int` | `{ actividadReciente(limit: 5) }` |

link.href = 'data:application/pdf;base64,' + base64;| 6️⃣ | `topAreas` | Top áreas con reportes | `limit: Int` | `{ topAreas(limit: 3) { area cantidad } }` |

link.download = 'reporte_analytics.pdf';| 7️⃣ | `promedioPuntuaciones` | Promedio de ratings | - | `{ promedioPuntuaciones }` |

link.click();| 8️⃣ | `etiquetasMasUsadas` | Etiquetas más frecuentes | `limit: Int` | `{ etiquetasMasUsadas(limit: 5) { clave valor } }` |

```| 9️⃣ | `reportesPorFecha` | Reportes en rango | `desde: String!, hasta: String!` | `{ reportesPorFecha(desde: "2024-01-01", hasta: "2024-12-31") { title } }` |

| 🔟 | `usuariosMasActivos` | Usuarios con más reportes | `limit: Int` | `{ usuariosMasActivos(limit: 3) { clave valor } }` |

---

---

## 🛠️ Tecnologías

### **Módulo 5: Exportación Compuesta**

- **Apollo Server** 4.x

- **TypeScript** con ES Modules| Query             | Descripción                                                                                                     | Parámetros                          | Ejemplo              |

- **Fetch API** para consultas REST| ----------------- | --------------------------------------------------------------------------------------------------------------- | ----------------------------------- | -------------------- |

- **pdfkit** para generación real de PDFs| `reportAnalytics` | **Datos completos de reporte** (reporte + comentarios + puntuaciones + archivos + usuario + categoría + estado) | `reporteId: ID!`, `formato: String` | Ver ejemplo abajo ⬇️ |

- **Patrón Datasource** para centralizar lógica REST

#### Ejemplo de `reportAnalytics`:

---

```graphql

## 📝 Notas Importantes{

  reportAnalytics(reporteId: "1", formato: "json") {

- ✅ Todas las queries consumen el **REST API** (`http://localhost:8000`)    reporte {

- ✅ Sin mutaciones (GraphQL es **solo lectura**)      id

- ✅ Modular: cada entidad en archivo separado      title

- ✅ 10 queries analíticas (3 por integrante + 1 equipo)      description

- ✅ Query compuesto `reportAnalytics` con **PDF REAL** descargable      status

- ✅ **REST API notifica automáticamente al WebSocket** cuando se crea/actualiza un reporte o comentario    }

    comentarios {

---      id

      content

## 🔗 Integración con WebSocket      date

    }

Cuando se ejecuta:    puntuaciones {

- `POST /reportes` → REST API notifica al WebSocket evento `new_report`      id

- `PUT /reportes/{id}` → REST API notifica evento `update_report`      value

- `POST /comentarios` → REST API notifica evento `comment_added`    }

    archivos {

Los clientes conectados al WebSocket (`ws://localhost:8080/ws?room=reports`) reciben las notificaciones en tiempo real.      id

      filename

---      url

    }

## 🧪 Probar Queries    usuario {

      id

Abre **http://localhost:4000** en el navegador y ejecuta:      name

      email

```graphql    }

# Probar estadísticas (Integrante 1)    categoria {

{      id

  statsReportes {      name

    total    }

    abiertos    estado {

    cerrados      id

    enProceso      name

  }    }

}    formato

    pdfBase64 # Si formato="pdf", contiene PDF en base64

# Probar analytics completo con PDF (Integrante 3)  }

{}

  reportAnalytics(reporteId: "1", formato: "pdf") {```

    reporte { title status }

    comentarios { content }---

    usuario { name }

    pdfBase64## 🛠️ Tecnologías

  }

}- **Apollo Server** 4.x

```- **TypeScript** con ES Modules

- **Fetch API** para consultas REST

---- **Patrón Datasource** para centralizar lógica REST



**Semana 6** - Sistema de Informes Universidad 🚀  ---

**Cumplimiento 100%** con requisitos del docente ✅

## 📝 Notas

- ✅ Todas las queries consumen el **REST API** (`http://localhost:8000`)
- ✅ Sin mutaciones (GraphQL es **solo lectura**)
- ✅ Modular: cada entidad en archivo separado
- ✅ 10 queries analíticas combinando múltiples entidades
- ✅ Query compuesto `reportAnalytics` con exportación a JSON/PDF

---

## 🧪 Probar Queries

Abre **http://localhost:4000** en el navegador y ejecuta:

```graphql
# Probar estadísticas
{
  statsReportes {
    total
    abiertos
    cerrados
    enProceso
  }
}

# Probar analytics completo
{
  reportAnalytics(reporteId: "1") {
    reporte {
      title
    }
    comentarios {
      content
    }
    usuario {
      name
    }
  }
}
````

---

**Semana 6** - Equipo Sistema de Informes 🚀
`````
``````
