import os
from typing import List

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Cargar variables para que estén disponibles antes de importar la app
load_dotenv(dotenv_path=".env.test", override=True)
load_dotenv(override=False)

# Elegir URL priorizando DATABASE_URL_TEST
_db_url = os.getenv("DATABASE_URL_TEST") or os.getenv("DATABASE_URL")
if not _db_url:
    raise RuntimeError(
        "DATABASE_URL(_TEST) no configurado. Define tu URL en .env.test o .env."
    )

# Si se usa URL de test y no hay DB_SCHEMA, usar 'test'
if _db_url.startswith("postgres") and os.getenv("DATABASE_URL_TEST") and not os.getenv("DB_SCHEMA"):
    os.environ["DB_SCHEMA"] = "test"

DB_SCHEMA = os.getenv("DB_SCHEMA", "public")

# Construir engine directo para tareas de mantenimiento (sin depender de db.py)
# Forzar sslmode=require si falta (sólo Postgres)
if _db_url.startswith("postgresql") and "sslmode=" not in _db_url:
    sep = '&' if '?' in _db_url else '?'
    _db_url = f"{_db_url}{sep}sslmode=require"

_engine = create_engine(_db_url, pool_pre_ping=True)


def pytest_sessionstart(session):
    """Antes de correr tests: preparar base de datos para Postgres o SQLite."""
    try:
        if _db_url.startswith("sqlite"):
            # Si es archivo SQLite, eliminarlo para tener un entorno limpio
            # Formatos típicos: sqlite:///./test.db  | sqlite:///C:/ruta/test.db | sqlite:///:memory:
            prefix = "sqlite:///"
            if _db_url.startswith("sqlite:///:memory:"):
                # Nada que limpiar en memoria
                return
            if _db_url.startswith(prefix):
                db_path = _db_url[len(prefix):]
                # Normalizar separadores de ruta en Windows
                db_path = db_path.replace('/', os.sep)
                abs_path = os.path.abspath(db_path)
                # Crear directorio padre si no existe
                os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                if os.path.exists(abs_path):
                    try:
                        os.remove(abs_path)
                    except Exception:
                        pass
            # No ejecutamos SQL de schema; main.py creará tablas al importar la app
            return

        # Postgres: limpiar esquema
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
    except OperationalError as exc:
        pytest.exit(
            "No se pudo conectar a la base de datos configurada para las pruebas. "
            "Revisa DATABASE_URL_TEST o tu conexión de red.\n"
            f"Detalle: {exc}",
            returncode=0,
        )


def pytest_sessionfinish(session, exitstatus):
    """Nada especial al terminar; las tablas quedan limpias por cada corrida."""
    pass
