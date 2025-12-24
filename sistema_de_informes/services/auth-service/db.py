import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

AUTH_DATABASE_URL = os.getenv("AUTH_DATABASE_URL")
if not AUTH_DATABASE_URL:
    raise ValueError("AUTH_DATABASE_URL no está configurada para auth-service")

engine = create_engine(
    AUTH_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
