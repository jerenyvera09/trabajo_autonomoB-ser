from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from db import Base

class ArchivoAdjunto(Base):
    __tablename__ = "archivos_adjuntos"
    id_archivo: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_reporte: Mapped[int] = mapped_column(Integer, ForeignKey("reportes.id_reporte"), nullable=False)
    nombre_archivo: Mapped[str] = mapped_column(String, nullable=False)
    tipo: Mapped[str | None] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False)

    reporte = relationship("Reporte", back_populates="archivos")
