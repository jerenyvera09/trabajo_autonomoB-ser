# 🧩 REST API — Integrante 1 (Python / FastAPI)

Implementación del **Servicio REST** correspondiente a la **Semana 4 – Commit 2**, completamente funcional y listo para evaluación.  
Incluye **autenticación JWT**, **CRUD completo por entidad**, **validaciones**, **manejo estructurado de errores**, y **documentación automática** (Swagger / ReDoc).  
Base de datos por defecto: **SQLite (local)**.

---

## ⚙️ 1) Requisitos e instalación

**Requisitos previos**

- Python **3.10+** (probado con **3.12**)
- Librerías listadas en [`requirements.txt`](requirements.txt)

**Instalación**

```bash
pip install -r requirements.txt
🚀 2) Configuración y ejecución
(Opcional) Copia el archivo de entorno:

bash
Copiar código
cp .env.example .env
Ajusta las variables según sea necesario:

JWT_SECRET: clave para firmar tokens

DATABASE_URL: URL de la base de datos (por defecto sqlite:///./app.db)

Ejecuta el servidor:

bash
Copiar código
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Endpoints principales

🌐 Health check → http://localhost:8000/

📘 Swagger UI → http://localhost:8000/docs

📕 ReDoc → http://localhost:8000/redoc

🔐 3) Autenticación rápida (JWT)
1️⃣ Registro de usuario

bash
Copiar código
curl -X POST http://localhost:8000/auth/register \
   -H "Content-Type: application/json" \
   -d '{"nombre":"Admin","email":"admin@uleam.edu.ec","password":"123456"}'
2️⃣ Login (obtener token)

bash
Copiar código
curl -X POST http://localhost:8000/auth/login \
   -H "Content-Type: application/json" \
   -d '{"email":"admin@uleam.edu.ec","password":"123456"}'
3️⃣ Usar token en rutas protegidas

bash
Copiar código
curl http://localhost:8000/usuarios \
   -H "Authorization: Bearer <ACCESS_TOKEN>"
🧱 4) Alcance y entidades cubiertas
CRUD completo (GET / POST / PUT / DELETE) protegido por JWT en:

/usuarios

/roles

/reportes

/categorias

/areas

/estados-reporte

/comentarios

/puntuaciones

/archivos-adjuntos

Endpoints públicos:

POST /auth/register

POST /auth/login

🧩 5) Validaciones y manejo de errores
Validaciones Pydantic: emails, longitudes mínimas, rangos de valores, etc.

Integridad referencial (400): verificación de claves foráneas en POST/PUT.

Conflictos (409): evita borrado de entidades con dependencias activas.

Errores estándar:

401 Unauthorized: token ausente o inválido

404 Not Found: recurso inexistente

409 Conflict: entidad relacionada no puede eliminarse

🧮 6) Matriz de cumplimiento (Docente → Evidencia en código)
Requisito	Evidencia / Archivo
CRUD completo	Routers: usuario, rol, reporte, categoria, area, estado, comentario, puntuacion, archivo
Autenticación / Autorización	auth.py, deps.py con Depends(Auth) en routers
Documentación REST	main.py — Swagger /docs y ReDoc /redoc
Validaciones / Errores	schemas/schemas.py + HTTPException (400/401/404/409)
Base de datos / ORM	db.py, modelos en entities/, tablas generadas en main.py
Alcance global	Integración futura: GraphQL + WebSockets + Frontend (Semanas 5–7)

🧾 7) Base de datos y ORM
ORM: SQLAlchemy 2.x (Declarative + relaciones).

Motor: SQLite (archivo local app.db).

Las tablas se crean automáticamente en el arranque del servidor (Base.metadata.create_all(bind=engine)).

Migración a Postgres o Supabase (Semana 5): solo requiere cambiar la variable DATABASE_URL.

📈 8) Próximos pasos (Semanas 5–7)
Integración con servicio GraphQL (consultas analíticas).

Servidor WebSockets (notificaciones en tiempo real).

Frontend React/Vue/Next consumiendo REST/GraphQL/WebSockets.

Documentación final de arquitectura y demo integrada.

Autora:
👩‍💻 Cinthia Zambrano — Integrante 1 (Python / FastAPI)
📚 Semana 4 — Commit 2
```
