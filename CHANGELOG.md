# Changelog

Historial de cambios del Sistema de Reportes de Infraestructura Universitaria.

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

---

## [Semana 7] - 2025-10-29

### 🎯 Entregables Finales

#### Added

- ✅ **Frontend**: READMEs semanales (S5, S6, S7) documentando progreso incremental
  - Semana 5: Setup e integración triple (REST + GraphQL + WebSocket)
  - Semana 6: CRUD completo, autenticación JWT, componentes reutilizables
  - Semana 7: Tests E2E, optimización de rendimiento, documentación completa
- ✅ **Scripts**: README completo documentando 5 scripts de automatización
  - `check_supabase.py` - Verificación de conexión DB
  - `clean_local.py` - Limpieza de datos de desarrollo
  - `e2e_week6.py` - Tests de integración completa
  - `query_gql.py` - Cliente GraphQL CLI
  - `reset_supabase_schema.py` - Reset de schema DB
- ✅ **Docs**: README índice central con arquitectura, diagramas y contratos de APIs
- ✅ **README raíz**: Convertido en portada ejecutiva con tabla de contenidos y badges
- ✅ **CHANGELOG.md**: Historial de cambios por semana (este archivo)

#### Improved

- 📝 Limpieza de carpeta `docs/` - Eliminados 15 archivos obsoletos (auditorías antiguas)
- 📝 Organización profesional de documentación por servicios
- 📝 Enlaces directos a READMEs semanales desde README raíz

#### Metrics

- **Commits**: +2 commits finales (documentación)
- **Archivos nuevos**: 6 (Frontend x3, Scripts x1, Docs x1, CHANGELOG x1)
- **Archivos eliminados**: 15 (docs obsoletos)
- **Líneas de documentación**: +1,000 líneas

---

## [Semana 6] - 2025-10-22

### 📊 Queries Analíticas y Dashboard

#### Added

- ✅ **GraphQL**: 11 queries analíticas distribuidas por integrante
  - Integrante 1 (Cinthia): `statsReportes`, `reportesPorArea`, `topAreas`
  - Integrante 2 (Carlos): `reportesPorCategoria`, `promedioPuntuaciones`, `etiquetasMasUsadas`
  - Integrante 3 (Jereny): `reportesPorUsuario`, `actividadReciente`, `usuariosMasActivos`
  - Equipo: `reportesPorEstado`, `reportesPorFecha`
- ✅ **GraphQL**: Query compuesta `reportAnalytics` con generación de PDF real (pdfkit)
- ✅ **Frontend**: Dashboard analítico con 4 KPIs + gráficos
- ✅ **Frontend**: Botones de descarga de PDF por reporte
- ✅ **WebSocket**: Eventos `update_report` para actualizaciones en tiempo real
- ✅ **REST API**: Validaciones robustas con Pydantic
- ✅ **Tests**: Suite E2E completa (`e2e_week6.py`)

#### Improved

- 📈 Performance del GraphQL con DataLoader para queries complejas
- 🎨 UI del dashboard con diseño responsivo
- 🔒 Seguridad con validación de tokens JWT en WebSocket

#### Metrics

- **Commits**: +5 commits (queries analíticas, dashboard, PDF)
- **Líneas de código**: +2,500 líneas (GraphQL resolvers + Frontend dashboard)
- **Tests**: 20+ tests E2E automatizados

---

## [Semana 5] - 2025-10-15

### 🔗 Integración Completa

#### Added

- ✅ **Frontend**: Aplicación React + TypeScript + Vite
- ✅ **Frontend**: Integración con REST API (fetch)
- ✅ **Frontend**: Integración con GraphQL (Apollo Client)
- ✅ **Frontend**: Conexión WebSocket para notificaciones en tiempo real
- ✅ **GraphQL**: Queries de interacción (comentarios, puntuaciones, etiquetas)
- ✅ **GraphQL**: Alias en inglés para compatibilidad con frontend
- ✅ **WebSocket**: Sistema de ping/pong para keep-alive
- ✅ **WebSocket**: Autenticación con tokens JWT
- ✅ **REST API**: Endpoint `/notify` para enviar eventos a WebSocket

#### Improved

- 🎨 UI moderna con tarjetas de reportes y badges de estado
- 🔔 Notificaciones animadas con auto-dismiss
- 🌐 CORS configurado en todos los servicios
- 📱 Diseño responsivo mobile-first

#### Metrics

- **Commits**: +4 commits (integración frontend, WebSocket auth)
- **Líneas de código**: +1,800 líneas (Frontend completo)
- **Servicios integrados**: 3 (REST + GraphQL + WebSocket)

---

## [Semana 4] - 2025-10-08

### 🛠️ Implementación de Servicios

#### Added

- ✅ **REST API**: CRUD básico de 7 entidades
- ✅ **REST API**: Autenticación JWT con login/register
- ✅ **GraphQL**: DataSource REST para consumir API
- ✅ **GraphQL**: Resolvers para entidades básicas (usuarios, reportes, categorías)
- ✅ **GraphQL**: Schema completo con tipos GraphQL
- ✅ **WebSocket**: Sistema de rooms para organizar conexiones
- ✅ **WebSocket**: Broadcast a clientes específicos por room

#### Improved

- 🔐 Seguridad con bcrypt para passwords
- ✅ Validación de datos con Pydantic
- 📚 Documentación automática con Swagger (FastAPI)

#### Metrics

- **Commits**: +6 commits (CRUD, auth, resolvers básicos)
- **Líneas de código**: +3,000 líneas (REST + GraphQL + WebSocket core)
- **Endpoints REST**: 25+ endpoints

---

## [Semana 3] - 2025-10-01

### 🏗️ Setup Inicial y Arquitectura

#### Added

- ✅ **Arquitectura**: Definición de microservicios (REST, GraphQL, WebSocket, Frontend)
- ✅ **REST API**: Setup FastAPI + SQLAlchemy + PostgreSQL/SQLite
- ✅ **GraphQL**: Setup Apollo Server + TypeScript
- ✅ **WebSocket**: Setup Go + Gorilla WebSocket
- ✅ **Base de Datos**: Schema con 10 tablas (Usuarios, Reportes, Comentarios, etc.)
- ✅ **Docs**: Diagramas de arquitectura y UML
- ✅ **READMEs**: Documentación inicial por servicio

#### Decisions

- 🐍 Python + FastAPI para REST (velocidad + tipado)
- 📊 TypeScript + Apollo para GraphQL (type-safety)
- ⚡ Go + Gorilla para WebSocket (concurrencia eficiente)
- ⚛️ React + Vite para Frontend (performance)
- 🐘 PostgreSQL para producción, SQLite para desarrollo

#### Metrics

- **Commits**: +3 commits (setup inicial)
- **Líneas de código**: +1,500 líneas (estructura base)
- **Servicios**: 4 servicios definidos

---

## Leyenda

- ✅ **Added**: Nueva funcionalidad
- 📝 **Changed**: Cambios en funcionalidad existente
- 🐛 **Fixed**: Corrección de bugs
- 🗑️ **Removed**: Funcionalidad eliminada
- 📈 **Improved**: Mejoras de performance o calidad
- 🔒 **Security**: Mejoras de seguridad
- 🎨 **UI/UX**: Mejoras de interfaz o experiencia de usuario

---

## Estadísticas del Proyecto

### Commits por Integrante

- **Jereny Vera**: 14 commits (WebSocket + Coordinación)
- **Carlos Campuzano**: 7 commits (GraphQL)
- **Cinthia Zambrano**: 2 commits (REST API)

### Líneas de Código (Total: ~10,000)

- **REST API**: ~3,500 líneas (Python)
- **GraphQL**: ~2,500 líneas (TypeScript)
- **WebSocket**: ~1,500 líneas (Go)
- **Frontend**: ~2,000 líneas (TypeScript/TSX)
- **Documentación**: ~500 líneas (Markdown)

### Archivos Importantes

- **READMEs**: 20+ archivos de documentación
- **Tests**: 25+ archivos de tests automatizados
- **Scripts**: 5 scripts de automatización
- **Diagramas**: 2 diagramas (arquitectura + UML)

---

**Última actualización**: 29 de octubre de 2025  
**Estado del proyecto**: ✅ Completado - Semana 7
