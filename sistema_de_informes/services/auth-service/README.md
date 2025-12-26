# Auth Service (Semana 1)

Microservicio exclusivo de autenticación para el sistema de informes.

## Tecnologías
- FastAPI
- SQLAlchemy
- python-jose (JWT)
- passlib (PBKDF2)
- PostgreSQL

## Endpoints
- POST /auth/register
- POST /auth/login
- POST /auth/logout
- POST /auth/refresh
- GET  /auth/me
- GET  /auth/validate (interno)

## Entorno
Variables en `.env` (ver `.env.example`):
- `AUTH_DATABASE_URL`: cadena de conexión a PostgreSQL
- `JWT_SECRET`, `JWT_ALG`
- `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_MINUTES`
- `RATE_LIMIT_LOGIN_ATTEMPTS`, `RATE_LIMIT_WINDOW_SECONDS`

## Ejecutar local
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Docker
Incluido `Dockerfile`. También soporte en `docker-compose.yml` en la raíz del repo.
