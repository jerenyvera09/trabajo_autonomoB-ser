from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from db import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    estado: Mapped[str] = mapped_column(String, default="ACTIVO")
    id_rol: Mapped[int | None] = mapped_column(Integer, ForeignKey("roles.id_rol"), nullable=True)

    rol = relationship("Rol", back_populates="usuarios")
    reportes = relationship("Reporte", back_populates="usuario")
    comentarios = relationship("Comentario", back_populates="usuario")
    puntuaciones = relationship("Puntuacion", back_populates="usuario")
