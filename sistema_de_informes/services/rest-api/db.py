from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (si existe)
load_dotenv()

# Modo híbrido: por defecto SQLite local en sistema_de_informes/db/app.db.
# Si se define DATABASE_URL (PostgreSQL/Supabase), se usa esa conexión.

_here = os.path.dirname(os.path.abspath(__file__))
_default_sqlite_path = os.path.normpath(os.path.join(_here, "..", "..", "db", "app.db"))
_default_sqlite_path_posix = _default_sqlite_path.replace("\\", "/")
_default_sqlite_url = f"sqlite:///{_default_sqlite_path_posix}"

DATABASE_URL = os.getenv("DATABASE_URL", _default_sqlite_url)

# Esquema de base de datos (por defecto: public) — sólo aplica para Postgres
DB_SCHEMA = os.getenv("DB_SCHEMA", "public")

is_sqlite = DATABASE_URL.startswith("sqlite")

if is_sqlite:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
else:
    # Configuración del engine para PostgreSQL/Supabase
    # Formato esperado: postgresql://usuario:password@host:5432/base
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        connect_args={
            "options": f"-csearch_path={DB_SCHEMA}"
        },
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
