from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Construir una URL SQLite por defecto que apunte al directorio compartido `db/`
# a nivel de `sistema_de_informes`. Esto evita que se recree `app.db` en el
# directorio actual si no se define DATABASE_URL explícitamente.
_here = os.path.dirname(os.path.abspath(__file__))
_default_db_path = os.path.normpath(os.path.join(_here, "..", "..", "db", "app.db"))
# Normalizar a formato compatible con SQLAlchemy en Windows (slashes hacia adelante)
_default_db_url = f"sqlite:///{_default_db_path.replace('\\', '/')}"

DATABASE_URL = os.getenv("DATABASE_URL", _default_db_url)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
