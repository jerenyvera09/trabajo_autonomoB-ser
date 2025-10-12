from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text
from db import Base

class Area(Base):
    __tablename__ = "areas"
    id_area: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_area: Mapped[str] = mapped_column(String, nullable=False)
    responsable: Mapped[str | None] = mapped_column(String, nullable=True)
    ubicacion: Mapped[str | None] = mapped_column(String, nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)

    reportes = relationship("Reporte", back_populates="area")
