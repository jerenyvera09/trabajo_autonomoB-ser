from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from db import Base

class Etiqueta(Base):
    __tablename__ = "etiquetas"
    id_etiqueta: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    color: Mapped[str | None] = mapped_column(String, nullable=True)
