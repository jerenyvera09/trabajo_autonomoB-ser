from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from db import Base

class Reporte(Base):
    __tablename__ = "reportes"
    id_reporte: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    ubicacion: Mapped[str | None] = mapped_column(String, nullable=True)
    id_categoria: Mapped[int | None] = mapped_column(Integer, ForeignKey("categorias.id_categoria"), nullable=True)
    id_area: Mapped[int | None] = mapped_column(Integer, ForeignKey("areas.id_area"), nullable=True)
    id_estado: Mapped[int | None] = mapped_column(Integer, ForeignKey("estados_reporte.id_estado"), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="reportes")
    categoria = relationship("Categoria", back_populates="reportes")
    area = relationship("Area", back_populates="reportes")
    estado_obj = relationship("EstadoReporte", back_populates="reportes")
    archivos = relationship("ArchivoAdjunto", back_populates="reporte", cascade="all, delete")
    comentarios = relationship("Comentario", back_populates="reporte", cascade="all, delete")
    puntuaciones = relationship("Puntuacion", back_populates="reporte", cascade="all, delete")
