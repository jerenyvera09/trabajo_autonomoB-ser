# 🚀 Servicio GraphQL - Semana 7

**Responsable:** Integrante 2 **CARLOS DELGADO CAMPUZANO**(TypeScript / Apollo Server)  
**Objetivo (Semana 7):** Consolidar entrega final, tests automatizados, documentación completa y preparación de demo para evaluación del docente.

---

## 🎯 Entregables - Semana 7

### 1. Suite de Tests Automatizados

**Ubicación:** `tests/reports.test.ts`

**Cobertura:**

- Tests unitarios de resolvers (10 entidades).
- Tests de queries analíticas (11 queries).
- Test de query compuesta `reportAnalytics` con PDF.
- Tests de integración con DataSource REST (mocks).

**Comando de ejecución:**

```bash
npm test
```

**Resultados esperados:** 95%+ de cobertura en resolvers y datasources.

---

### 2. Documentación Completa

**Archivos generados:**

- `docs/graphql_queries_reference.md` — Referencia completa de todas las queries con ejemplos.
- `docs/graphql_schema.graphql` — Schema completo exportado.
- `docs/graphql_analytics_distribution.md` — Distribución de queries analíticas por integrante.

**Contenido clave:**

- Tabla de queries con descripción, parámetros y ejemplos.
- Diagramas de flujo: Frontend → GraphQL → REST.
- Contratos de datos para cada entidad.

---

### 3. Demo Preparada

**Script de demo** (`scripts/demo_graphql.sh` o `demo_graphql.cmd`):

```bash
# 1. Levantar servicios
cd sistema_de_informes/services/rest-api
python -m uvicorn main:app --reload &

cd ../graphql
npm run dev &

cd ../ws
go run main.go &

cd ../../apps/frontend
npm run dev

# 2. Abrir Playground GraphQL
start http://localhost:4000

# 3. Ejecutar query de demo
# Ver script en docs/demo_queries.graphql
```

**Queries de demo preparadas:**

1. `statsReportes` — Mostrar estadísticas generales.
2. `reportAnalytics(reporteId: "1", formato: "pdf")` — Generar PDF de reporte completo.
3. `actividadReciente(limit: 10)` — Mostrar actividad reciente mezclada.

---

### 4. Evidencias de Commits Semanales

**Comando para mostrar commits por integrante:**

```bash
git log --author="Carlos" --oneline --since="2024-10-01" --until="2024-10-29"
```

**Resultado esperado:** Commits semanales documentando progreso incremental (S3 → S4 → S5 → S6 → S7).

---

## ✅ Checklist de validación

- [x] 11 queries analíticas implementadas y distribuidas.
- [x] Query compuesta `reportAnalytics` con PDF funcional.
- [x] Tests automatizados (95%+ cobertura).
- [x] Documentación completa en `docs/`.
- [x] Alias en inglés para frontend.
- [x] CORS configurado para integración con React.
- [x] Demo reproducible con script `demo_graphql.sh`.
- [x] Evidencia de commits semanales en `git log`.

---

## 🧾 Documentos para el docente

1. **READMEs semanales** (S3 → S7): Evidencia de progreso incremental.
2. **Referencia de queries**: `docs/graphql_queries_reference.md`.
3. **Schema exportado**: `docs/graphql_schema.graphql`.
4. **Script de demo**: `scripts/demo_graphql.sh`.
5. **Commits por integrante**: `git shortlog -sn --all`.

---

## 🔧 Despliegue (opcional)

Si se requiere despliegue en producción:

- **Heroku / Railway**: Configurar `Procfile` con `npm start`.
- **Docker**: `Dockerfile` con Node.js 18+ Alpine.
- **Variables de entorno**: `REST_BASE_URL`, `REST_API_TOKEN`, `PORT`.

---

**Semana 7 completada — GraphQL listo para evaluación final.**
