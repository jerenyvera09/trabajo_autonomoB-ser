from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text
from db import Base

class Categoria(Base):
    __tablename__ = "categorias"
    id_categoria: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    prioridad: Mapped[str | None] = mapped_column(String, nullable=True)  # BAJA/MEDIA/ALTA
    estado: Mapped[str] = mapped_column(String, default="ACTIVO")

    reportes = relationship("Reporte", back_populates="categoria")
