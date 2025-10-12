from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, Boolean
from db import Base

class EstadoReporte(Base):
    __tablename__ = "estados_reporte"
    id_estado: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    color: Mapped[str | None] = mapped_column(String, nullable=True)
    orden: Mapped[int | None] = mapped_column(Integer, nullable=True)
    es_final: Mapped[bool] = mapped_column(Boolean, default=False)

    reportes = relationship("Reporte", back_populates="estado_obj")
