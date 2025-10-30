# 🚀 Servicio GraphQL - Semana 5

**Responsable:** Integrante 2 **CARLOS DELGADO CAMPUZANO**(TypeScript / Apollo Server)  
**Objetivo (Semana 5):** Completar las queries de interacción (comentarios, puntuaciones, etiquetas) y agregar alias en inglés para compatibilidad con el frontend.

---

## ✅ Tareas completadas - Semana 5

1. **Resolvers de interacción** (Módulo 3):
   - `comentarios.ts`: queries `comentarios`, `comentario(id)`, `comentariosByReporte`, `comentariosByUsuario`.
   - `puntuaciones.ts`: queries `puntuaciones`, `puntuacion(id)`, `puntuacionesByReporte`.
   - `etiquetas.ts`: queries `etiquetas`, `etiqueta(id)`.

2. **Alias en inglés para frontend**:
   - `reports` → `reportes`
   - `reportsAnalytics` → `reportesAnalytics` (preparado para Semana 6)
   - `categories` → `categorias`
   - `states` → `estados`
   - `users` → `usuarios`
   - `comments` → `comentarios`
   - `ratings` → `puntuaciones`
   - `files` → `archivosAdjuntos`
   - `tags` → `etiquetas`

   **Beneficio:** El frontend puede usar nombres en inglés sin modificar el schema original en español.

3. **Queries de paginación y filtrado**:
   - `reports(limit, offset)` → retorna `ReportConnection { items, total, limit, offset }`.
   - Filtros por estado, prioridad, categoría, área, usuario.

4. **Pruebas de integración con Frontend**:
   - React + Apollo Client conecta exitosamente a `http://localhost:4000`.
   - Queries probadas: `reports`, `categories`, `states`, `comments`.

---

## 🧪 Ejemplos de queries probadas

```graphql
# Alias en inglés: consultar reportes con paginación
{
  reports(limit: 10, offset: 0) {
    items {
      id
      title
      status
    }
    total
  }
}

# Consultar comentarios de un reporte
{
  comments(reporteId: "1") {
    id
    content
    createdAt
    user {
      name
    }
  }
}

# Consultar puntuaciones promedio (preparado para analíticas S6)
{
  ratings {
    id
    value
    reporteId
  }
}
```

---

## 🔧 Configuración de CORS

Agregado middleware CORS en `src/index.ts` para permitir peticiones desde frontend (puerto 3000).

```typescript
const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [ApolloServerPluginLandingPageLocalDefault()],
});

await server.start();
const app = express();
app.use(cors({ origin: "http://localhost:3000" }));
app.use("/graphql", expressMiddleware(server));
```

---

## 🔜 Próximos pasos (Semana 6)

- Implementar 11 queries analíticas distribuidas por integrante.
- Crear query compuesta `reportAnalytics` con generación de PDF (pdfkit).
- Probar integración E2E: REST → GraphQL → Frontend.

---

**Semana 5 completada — GraphQL con 10 entidades, 30+ queries y compatibilidad frontend.**
