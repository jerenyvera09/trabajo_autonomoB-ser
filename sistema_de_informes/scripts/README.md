# 🔧 Scripts de Automatización y Testing

Colección de scripts Python para automatización, testing y mantenimiento del sistema de reportes.

---

## 📋 Scripts disponibles

### 1. `check_supabase.py` - Verificación de conexión a base de datos

**Propósito:** Verificar que la conexión a Supabase/PostgreSQL esté configurada correctamente.

**Uso:**

```bash
cd sistema_de_informes/scripts
python check_supabase.py
```

**Salida esperada:**

```
✅ Conexión a Supabase exitosa
✅ Base de datos: postgres
✅ Tablas encontradas: 10
```

**Cuándo ejecutar:**

- Después de configurar variables de entorno (`DATABASE_URL`)
- Antes de ejecutar migraciones
- Para troubleshooting de conexión DB

---

### 2. `clean_local.py` - Limpieza de datos locales

**Propósito:** Limpiar base de datos local (SQLite) para desarrollo y testing.

**Uso:**

```bash
python clean_local.py
```

**Operaciones:**

- Elimina todos los registros de tablas
- Resetea secuencias de IDs
- Mantiene estructura de tablas intacta

**⚠️ ADVERTENCIA:** Solo usar en ambiente de desarrollo. NO ejecutar en producción.

**Cuándo ejecutar:**

- Antes de ejecutar tests E2E limpios
- Cuando necesites resetear datos de prueba
- Durante desarrollo para limpiar datos basura

---

### 3. `e2e_week6.py` - Tests E2E de integración completa

**Propósito:** Validar integración completa entre los 3 servicios (REST + GraphQL + WebSocket).

**Flujo de prueba:**

1. Verifica que REST API esté corriendo (`GET /health`)
2. Verifica que GraphQL esté corriendo (query de healthcheck)
3. Verifica que WebSocket esté corriendo
4. Crea un reporte vía REST (`POST /api/v1/reports`)
5. Consulta el reporte vía GraphQL
6. Envía notificación vía WebSocket (`POST /notify/reports`)
7. Valida que la notificación se recibió correctamente

**Uso:**

```bash
python e2e_week6.py
```

**Salida esperada:**

```
🧪 Iniciando tests E2E - Semana 6
✅ REST API: OK (http://localhost:8000)
✅ GraphQL: OK (http://localhost:4000)
✅ WebSocket: OK (ws://localhost:8080)
✅ Test 1: Crear reporte vía REST → ID: 123
✅ Test 2: Consultar reporte vía GraphQL → Encontrado
✅ Test 3: Notificación WebSocket → Enviada y recibida
🎉 Todos los tests pasaron exitosamente!
```

**Cuándo ejecutar:**

- Antes de hacer commit de cambios importantes
- Como parte de CI/CD pipeline
- Para validar que todos los servicios funcionan juntos

---

### 4. `query_gql.py` - Cliente para probar queries GraphQL

**Propósito:** Ejecutar queries GraphQL desde línea de comandos sin necesidad de abrir Playground.

**Uso básico:**

```bash
# Query predefinida (stats de reportes)
python query_gql.py

# Query personalizada
python query_gql.py --query "{ reports { id title } }"
```

**Queries predefinidas:**

```python
# Ver estadísticas de reportes
python query_gql.py --stats

# Ver reportes por área
python query_gql.py --area "TI"

# Ver actividad reciente
python query_gql.py --recent --limit 10
```

**Cuándo ejecutar:**

- Para probar queries rápidamente sin abrir navegador
- En scripts de automatización que necesiten datos de GraphQL
- Para debugging de queries complejas

---

### 5. `reset_supabase_schema.py` - Reset completo del schema en Supabase

**Propósito:** Recrear todas las tablas en Supabase/PostgreSQL desde cero.

**⚠️ ADVERTENCIA:** Elimina TODOS los datos. Solo usar en desarrollo.

**Uso:**

```bash
python reset_supabase_schema.py
```

**Operaciones:**

1. Drop de todas las tablas existentes
2. Recreación de tablas desde `services/rest-api/sql/schema_postgres.sql`
3. Inserción de datos de prueba (opcional)

**Cuándo ejecutar:**

- Cuando cambias el schema de la base de datos
- Para sincronizar schema local con producción
- Antes de ejecutar migraciones importantes

---

## 🛠️ Requisitos

**Dependencias Python:**

```bash
pip install requests python-dotenv psycopg2-binary websocket-client
```

**Variables de entorno necesarias:**

```env
DATABASE_URL=postgresql://user:pass@host:port/dbname
REST_BASE_URL=http://localhost:8000
GRAPHQL_URL=http://localhost:4000
WS_URL=ws://localhost:8080
```

---

## 📊 Uso en CI/CD

**Ejemplo de GitHub Actions workflow:**

```yaml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Start services
        run: |
          cd services/rest-api && uvicorn main:app &
          cd services/graphql && npm run dev &
          cd services/ws && go run main.go &

      - name: Run E2E tests
        run: python scripts/e2e_week6.py
```

---

## 📅 Scripts creados por semana

**Semana 4:**

- `check_supabase.py` - Validación de conexión DB

**Semana 5:**

- `query_gql.py` - Cliente GraphQL CLI

**Semana 6:**

- `e2e_week6.py` - Tests de integración completa
- `clean_local.py` - Limpieza de datos de desarrollo

**Semana 7:**

- `reset_supabase_schema.py` - Reset de schema DB

---

## 🔐 Buenas prácticas

1. **Nunca ejecutar scripts destructivos en producción** (`clean_local.py`, `reset_supabase_schema.py`)
2. **Usar variables de entorno** en lugar de hardcodear URLs/credenciales
3. **Agregar logging** para troubleshooting (`print` con emojis para claridad)
4. **Validar prerequisitos** antes de ejecutar operaciones (verificar que servicios estén corriendo)
5. **Documentar cada script** con docstrings en el código

---

**Scripts documentados — Automatización lista para desarrollo y CI/CD.**
