# 🎯 Guía de Demostración - Cumplimiento 100%

**Sistema de Informes - ULEAM**  
**Docente:** John Cevallos  
**Fecha:** 29 de octubre de 2025

---

## 🚀 Pasos para Demostrar el 100% de Cumplimiento

### **1. Iniciar Todos los Servicios**

```bash
# Terminal 1: REST API (Puerto 8000)
cd sistema_de_informes\services\rest-api
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: GraphQL (Puerto 4000)
cd sistema_de_informes\services\graphql
npm run dev

# Terminal 3: WebSocket (Puerto 8080)
cd sistema_de_informes\services\ws
go run main.go

# Terminal 4: Frontend (Puerto 5173)
cd sistema_de_informes\apps\frontend
npm run dev
```

**Verificar que todos estén corriendo:**

- REST: http://localhost:8000/docs
- GraphQL: http://localhost:4000
- WebSocket: ws://localhost:8080
- Frontend: http://localhost:5173

---

### **2. Demostrar Dashboard Analítico (Requisito Crítico)**

**URL:** http://localhost:5173

**Qué mostrar al docente:**

1. 4 KPIs superiores
2. Top 3 Áreas con medallas
3. Promedio de Puntuaciones con color
4. Botón “📊 Actualizar Analytics”

**Explicación:** datos vienen de `statsReportes`, `topAreas`, `promedioPuntuaciones`.

---

### **3. Descarga de PDF por Reporte**

1. En la sección REST o GraphQL, usar “📄 Descargar Reporte PDF”.
2. Se descarga un PDF real generado por `reportAnalytics` (pdfkit) con 6 secciones.

---

### **4. Integración WebSocket → Frontend**

1. Abrir dos ventanas del frontend.
2. Crear un reporte por REST:

```bash
curl -X POST http://localhost:8000/api/v1/reports \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Test Docente\",\"description\":\"Demo\",\"status\":\"Abierto\"}"
```

3. Ambas ventanas muestran notificación y KPIs se actualizan.

---

### **5. Queries Analíticas en Playground (http://localhost:4000)**

```graphql
{
  statsReportes { total abiertos cerrados enProceso }
  topAreas(limit: 3) { area cantidad }
  promedioPuntuaciones
}
```

```graphql
{
  reportesPorEstado(estado: "Abierto") { id title status }
}
```

```graphql
{
  reportAnalytics(reporteId: "1", formato: "pdf") { pdfBase64 reporte { title } }
}
```

---

### **6. Confirmar que GraphQL NO duplica CRUD**

No existen mutaciones; solo `type Query`.

---

### **7. Mostrar Documentación**

- README raíz (índice + quickstart)
- services/graphql/README.md (queries y distribución)
- services/ws/README.md (eventos y endpoints)

---

## 📊 Checklist de Demostración

| Ítem | Descripción                           | ✅ |
| ---- | ------------------------------------- | - |
| 1    | KPIs visibles                         | ☐ |
| 2    | Top 3 Áreas con medallas              | ☐ |
| 3    | Promedio con color                    | ☐ |
| 4    | PDF descargable                        | ☐ |
| 5    | PDF con 6 secciones                   | ☐ |
| 6    | WebSocket conectado (verde)           | ☐ |
| 7    | Crear reporte actualiza dashboard     | ☐ |
| 8    | Dos ventanas reciben notificación     | ☐ |
| 9    | 11 queries analíticas operativas      | ☐ |
| 10   | Sin mutaciones en GraphQL             | ☐ |
| 11   | Documentación por integrante          | ☐ |

---

## 🎤 Discurso breve (7 min)

1. Arquitectura y responsabilidades del equipo.
2. Dashboard y analytics (GraphQL → REST).
3. PDF por reporte (reportAnalytics + pdfkit).
4. WS en tiempo real (REST → WS → Frontend).
5. Cierre: 100% de cumplimiento y dudas.
