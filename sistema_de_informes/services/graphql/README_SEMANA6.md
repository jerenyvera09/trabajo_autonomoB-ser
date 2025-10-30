# 🚀 Servicio GraphQL - Semana 6

**Responsable:** Integrante 2 **CARLOS DELGADO CAMPUZANO** (TypeScript / Apollo Server)  
**Objetivo (Semana 6):** Implementar las 11 queries analíticas distribuidas por integrante, crear la query compuesta `reportAnalytics` con generación de PDF real y completar pruebas E2E.

---

## ✅ Tareas completadas - Semana 6

### 1. Queries Analíticas (Módulo 4: `analytics.ts`)

**Distribuidas por integrante según planificación:**

#### Integrante 1 (Cinthia Zambrano - REST API):

1. `statsReportes` — Estadísticas generales (total, abiertos, cerrados, en proceso).
2. `reportesPorArea` — Filtrar reportes por área específica.
3. `topAreas` — Top N áreas con más reportes.

#### Integrante 2 (Carlos Campuzano - GraphQL):

4. `reportesPorCategoria` — Filtrar reportes por categoría.
5. `promedioPuntuaciones` — Calcular promedio de todas las puntuaciones.
6. `etiquetasMasUsadas` — Top N etiquetas más frecuentes.

#### Integrante 3 (Jereny Vera - WebSocket):

7. `reportesPorUsuario` — Reportes creados por un usuario específico.
8. `actividadReciente` — Actividad mezclada (reportes + comentarios ordenados por fecha).
9. `usuariosMasActivos` — Top N usuarios con más reportes creados.

#### Equipo:

10. `reportesPorEstado` — Filtrar reportes por estado específico.
11. `reportesPorFecha` — Filtrar reportes en un rango de fechas.

---

### 2. Query Compuesta `reportAnalytics` (Módulo 5: `export.ts`)

**Características:**

- Agrega datos de **7 entidades REST**:
  - Reporte principal
  - Comentarios
  - Puntuaciones
  - Archivos adjuntos
  - Usuario creador
  - Categoría
  - Estado
- Genera **PDF real** con `pdfkit` en formato base64.
- Exporta como JSON (default) o PDF (`formato="pdf"`).

**Ejemplo de uso:**

```graphql
{
  reportAnalytics(reporteId: "1", formato: "pdf") {
    reporte {
      id
      title
      description
      status
      priority
    }
    comentarios {
      id
      content
      author {
        name
      }
    }
    puntuaciones {
      id
      value
    }
    archivos {
      id
      filename
      url
    }
    pdfBase64 # Solo si formato="pdf"
  }
}
```

**Resultado:** Retorna objeto JSON completo + campo `pdfBase64` con PDF descargable.

---

## 🧪 Pruebas realizadas

### Query analítica: `statsReportes`

```graphql
{
  statsReportes {
    total
    abiertos
    cerrados
    enProceso
  }
}
```

**Resultado:**

```json
{
  "data": {
    "statsReportes": {
      "total": 45,
      "abiertos": 12,
      "cerrados": 28,
      "enProceso": 5
    }
  }
}
```

### Query compuesta: `reportAnalytics`

```graphql
{
  reportAnalytics(reporteId: "3", formato: "json") {
    reporte {
      title
      status
    }
    comentarios {
      content
    }
    puntuaciones {
      value
    }
  }
}
```

**Resultado:** JSON con datos agregados de múltiples entidades.

---

## 🔧 Dependencias agregadas

```json
{
  "dependencies": {
    "pdfkit": "^0.14.0",
    "apollo-server": "^4.9.5",
    "graphql": "^16.8.1"
  }
}
```

---

## 🔜 Próximos pasos (Semana 7)

- Crear suite de tests automatizados con Jest.
- Generar documentación completa de todas las queries con ejemplos.
- Preparar demo E2E: Frontend → GraphQL → REST → WebSocket.

---

**Semana 6 completada — GraphQL con 11 queries analíticas y exportación PDF.**
