import os
from typing import List
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables para que estén disponibles antes de importar la app
load_dotenv(dotenv_path=".env.test", override=True)
load_dotenv(override=False)

# Elegir URL priorizando DATABASE_URL_TEST
_db_url = os.getenv("DATABASE_URL_TEST") or os.getenv("DATABASE_URL")
if not _db_url or not _db_url.startswith("postgres"):
    raise RuntimeError(
        "DATABASE_URL(_TEST) no configurado o no es Postgres. Define tu URL de Supabase en .env.test o .env."
    )

# Si se usa URL de test y no hay DB_SCHEMA, usar 'test'
if os.getenv("DATABASE_URL_TEST") and not os.getenv("DB_SCHEMA"):
    os.environ["DB_SCHEMA"] = "test"

DB_SCHEMA = os.getenv("DB_SCHEMA", "public")

# Construir engine directo para tareas de mantenimiento (sin depender de db.py)
# Forzar sslmode=require si falta
if _db_url.startswith("postgresql") and "sslmode=" not in _db_url:
    sep = '&' if '?' in _db_url else '?'
    _db_url = f"{_db_url}{sep}sslmode=require"

_engine = create_engine(_db_url, pool_pre_ping=True)


def pytest_sessionstart(session):
    """Antes de correr tests: asegurar esquema y limpiar tablas del esquema."""
    schema = DB_SCHEMA
    with _engine.begin() as conn:
        # Crear esquema si no existe (ignorar errores si falta permiso)
        try:
            if schema and schema != "public":
                conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
        except Exception:
            pass
        # Establecer search_path
        try:
            conn.execute(text(f'SET search_path TO "{schema}", public'))
        except Exception:
            pass
        # Obtener tablas y truncar
        result = conn.execute(
            text(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = :schema AND table_type='BASE TABLE'
                """
            ),
            {"schema": schema},
        )
        tables: List[str] = [row[0] for row in result]
        if tables:
            joined = ", ".join([f'"{schema}"."{t}"' for t in tables])
            conn.execute(text(f"TRUNCATE TABLE {joined} RESTART IDENTITY CASCADE"))


def pytest_sessionfinish(session, exitstatus):
    """Nada especial al terminar; las tablas quedan limpias por cada corrida."""
    pass
