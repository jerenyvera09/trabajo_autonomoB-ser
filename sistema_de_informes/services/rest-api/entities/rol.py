from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text
from db import Base

class Rol(Base):
    __tablename__ = "roles"
    id_rol: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_rol: Mapped[str] = mapped_column(String, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String, nullable=True)
    permisos: Mapped[str | None] = mapped_column(Text, nullable=True)

    usuarios = relationship("Usuario", back_populates="rol")
