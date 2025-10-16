"""
Script de verificación de conexión a Supabase.
- Carga .env y .env.test
- Reutiliza el engine de services/rest-api/db.py
- Imprime: versión de Postgres, base actual, schema actual, search_path y conteo de tablas del schema.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import text

ROOT = Path(__file__).resolve().parents[1]
REST_DIR = ROOT / "services" / "rest-api"

# Cargar entornos
load_dotenv(REST_DIR / ".env.test", override=True)
load_dotenv(REST_DIR / ".env", override=False)

# Asegurar que services/rest-api esté en sys.path para importar db.py
sys.path.insert(0, str(REST_DIR))

# Importar engine ya configurado y DB_SCHEMA
import db  # type: ignore

print("== Supabase connection check ==")
print(f"DATABASE_URL startswith postgres: {db.DATABASE_URL.startswith('postgres')}")
print(f"DB_SCHEMA: {os.getenv('DB_SCHEMA', 'public')}")

with db.engine.connect() as conn:
    ver = conn.execute(text("select version()"))
    print("version:", ver.scalar())

    curr_db = conn.execute(text("select current_database()"))
    print("current_database:", curr_db.scalar())

    curr_schema = conn.execute(text("select current_schema()"))
    print("current_schema:", curr_schema.scalar())

    sp = conn.execute(text("show search_path"))
    print("search_path:", sp.scalar())

    cnt = conn.execute(
        text(
            """
            select count(*) from information_schema.tables
            where table_schema = current_schema() and table_type='BASE TABLE'
            """
        )
    )
    print("tables_in_schema:", cnt.scalar())

print("OK: conexión y metadatos obtenidos correctamente.")
