# 🚀 Servicio GraphQL - Semana 4

**Responsable:** Integrante 2 **CARLOS DELGADO CAMPUZANO** (TypeScript / Apollo Server)  
**Objetivo (Semana 4):** Implementar el DataSource REST, crear resolvers para las entidades básicas y configurar el servidor Apollo con queries de lectura.

---

## ✅ Tareas completadas - Semana 4

1. **DataSource REST implementado** (`src/datasources/rest.ts`):
   - Cliente HTTP para consumir el API REST (puerto 8000).
   - Fallbacks automáticos: `/api/v1/<en>` → `/api/v1/<es>` si no existe la ruta en inglés.
   - Soporte para autenticación Bearer (`REST_API_TOKEN`).

2. **Resolvers de entidades básicas**:
   - **Módulo 1 - Autenticación**:
     - `usuarios.ts`: queries `usuarios`, `usuario(id)`, `usuariosByStatus`.
     - `roles.ts`: queries `roles`, `rol(id)`.
   - **Módulo 2 - Reportes**:
     - `reportes.ts`: queries `reportes`, `reporte(id)`, `reportesByStatus`, `reportesByPriority`.
     - `categorias.ts`: queries `categorias`, `categoria(id)`, `categoriasByPriority`.
     - `areas.ts`: queries `areas`, `area(id)`, `areasByResponsable`.
     - `estados.ts`: queries `estados`, `estado(id)`, `estadosFinal`.
     - `archivosAdjuntos.ts`: queries `archivosAdjuntos`, `archivoAdjunto(id)`, `archivosByReporte`.

3. **Schema GraphQL** (`src/schema.ts`):
   - Definición de tipos para 7 entidades: `Usuario`, `Rol`, `Reporte`, `Categoria`, `Area`, `Estado`, `ArchivoAdjunto`.
   - Queries de lectura para cada entidad.

4. **Servidor Apollo configurado** (`src/index.ts`):
   - Apollo Server v4 con Playground habilitado.
   - Variables de entorno: `REST_BASE_URL`, `REST_API_TOKEN`.
   - Puerto: 4000.

---

## 🧪 Pruebas realizadas

```graphql
# Consultar todos los reportes
{
  reportes {
    id
    title
    status
    priority
  }
}

# Consultar un reporte específico con su categoría y estado
{
  reporte(id: "1") {
    id
    title
    description
    status
    priority
    categoria {
      name
    }
    estado {
      name
    }
  }
}

# Filtrar reportes por estado
{
  reportesByStatus(status: "Abierto") {
    id
    title
    priority
  }
}
```

**Resultados:** Todas las queries funcionan correctamente consumiendo datos del REST API.

---

## 🔜 Próximos pasos (Semana 5)

- Implementar resolvers de interacción (comentarios, puntuaciones, etiquetas).
- Agregar queries de filtrado avanzado.
- Probar integración con Frontend (React + Apollo Client).

---

**Semana 4 completada — GraphQL operativo con 7 entidades y 20+ queries.**
