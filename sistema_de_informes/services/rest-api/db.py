from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración para Supabase (PostgreSQL)
# La variable DATABASE_URL debe estar configurada en el archivo .env
# Formato: postgresql://usuario:password@host.supabase.co:5432/postgres
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "❌ DATABASE_URL no está configurada. "
        "Por favor, configura tu conexión a Supabase en el archivo .env"
    )

# Esquema de base de datos (por defecto: public)
DB_SCHEMA = os.getenv("DB_SCHEMA", "public")

# Configuración del engine para PostgreSQL/Supabase
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args={
        "options": f"-csearch_path={DB_SCHEMA}"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
