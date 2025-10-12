from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, DateTime, ForeignKey
from datetime import datetime
from db import Base

class Comentario(Base):
    __tablename__ = "comentarios"
    id_comentario: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_reporte: Mapped[int] = mapped_column(Integer, ForeignKey("reportes.id_reporte"), nullable=False)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="comentarios")
    reporte = relationship("Reporte", back_populates="comentarios")
