from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, ForeignKey
from datetime import datetime
from db import Base

class Puntuacion(Base):
    __tablename__ = "puntuaciones"
    id_puntuacion: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_reporte: Mapped[int] = mapped_column(Integer, ForeignKey("reportes.id_reporte"), nullable=False)
    valor: Mapped[int] = mapped_column(Integer, nullable=False)  # 1..5
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="puntuaciones")
    reporte = relationship("Reporte", back_populates="puntuaciones")
