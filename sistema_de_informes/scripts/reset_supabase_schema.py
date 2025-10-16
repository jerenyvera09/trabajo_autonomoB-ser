"""
Limpia por completo un esquema de Supabase (TRUNCATE RESTART IDENTITY CASCADE).
- Usa variables del REST API: .env y .env.test
- Esquema por defecto: public (puedes sobreescribir con DB_SCHEMA o --schema=nombre)
"""
from __future__ import annotations
import os
import sys
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
REST_DIR = ROOT / "services" / "rest-api"

# Cargar entornos (primero .env, luego .env.test si quieres limpiar test)
load_dotenv(REST_DIR / ".env", override=False)
load_dotenv(REST_DIR / ".env.test", override=False)

# Parámetros
schema = os.getenv("DB_SCHEMA", "public")
if len(sys.argv) > 1 and sys.argv[1].startswith("--schema="):
    schema = sys.argv[1].split("=", 1)[1]

# Usar DATABASE_URL (no la de test) por defecto para limpiar public
db_url = os.getenv("DATABASE_URL")
if not db_url or not db_url.startswith("postgres"):
    print("ERROR: DATABASE_URL no configurada o no es postgres. Define en services/rest-api/.env")
    sys.exit(1)

# Forzar sslmode=require si falta
if db_url.startswith("postgresql") and "sslmode=" not in db_url:
    sep = '&' if '?' in db_url else '?'
    db_url = f"{db_url}{sep}sslmode=require"

engine = create_engine(db_url, pool_pre_ping=True)


def list_tables(schema: str) -> List[str]:
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = :schema AND table_type='BASE TABLE'
                ORDER BY table_name
                """
            ),
            {"schema": schema},
        )
        return [r[0] for r in rows]


def count_rows(schema: str, table: str) -> int:
    with engine.connect() as conn:
        r = conn.execute(text(f'SELECT COUNT(*) FROM "{schema}"."{table}"'))
        return int(r.scalar() or 0)


def truncate_schema(schema: str):
    tables = list_tables(schema)
    if not tables:
        print(f"No hay tablas en el esquema '{schema}'. Nada que limpiar.")
        return
    with engine.begin() as conn:
        joined = ", ".join([f'"{schema}"."{t}"' for t in tables])
        conn.execute(text(f"TRUNCATE TABLE {joined} RESTART IDENTITY CASCADE"))
    print(f"Esquema '{schema}' truncado: {len(tables)} tablas limpiadas.")


def main():
    print(f"== Limpieza de esquema Supabase ==\nSchema objetivo: {schema}")
    tables = list_tables(schema)
    if not tables:
        print("No hay tablas, saltando limpieza.")
        return
    print("Tablas encontradas:", ", ".join(tables))
    before = {t: count_rows(schema, t) for t in tables}
    total_before = sum(before.values())
    print("Filas antes:", total_before, before)
    truncate_schema(schema)
    after = {t: count_rows(schema, t) for t in tables}
    total_after = sum(after.values())
    print("Filas después:", total_after, after)
    print("OK")


if __name__ == "__main__":
    main()
