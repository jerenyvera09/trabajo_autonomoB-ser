from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ---- Roles ----
class RolCreate(BaseModel):
    nombre_rol: str = Field(min_length=2)
    descripcion: Optional[str] = None
    permisos: Optional[str] = None
class RolUpdate(BaseModel):
    nombre_rol: Optional[str] = Field(default=None, min_length=2)
    descripcion: Optional[str] = None
    permisos: Optional[str] = None
class RolOut(BaseModel):
    id_rol: int
    nombre_rol: str
    descripcion: Optional[str]
    permisos: Optional[str]
    class Config: from_attributes = True

# ---- Usuarios ----
class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=6)
    id_rol: Optional[int] = None
class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2)
    estado: Optional[str] = None
    id_rol: Optional[int] = None
class UsuarioOut(BaseModel):
    id_usuario: int
    nombre: str
    email: EmailStr
    estado: str
    id_rol: Optional[int]
    class Config: from_attributes = True

class LoginIn(BaseModel):
    email: EmailStr
    password: str
class TokenOut(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"

# ---- Categoria ----
class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    prioridad: Optional[str] = None
    estado: Optional[str] = "ACTIVO"
class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    prioridad: Optional[str] = None
    estado: Optional[str] = None
class CategoriaOut(BaseModel):
    id_categoria: int
    nombre: str
    descripcion: Optional[str]
    prioridad: Optional[str]
    estado: str
    class Config: from_attributes = True

# ---- Area ----
class AreaCreate(BaseModel):
    nombre_area: str
    responsable: Optional[str] = None
    ubicacion: Optional[str] = None
    descripcion: Optional[str] = None
class AreaUpdate(BaseModel):
    nombre_area: Optional[str] = None
    responsable: Optional[str] = None
    ubicacion: Optional[str] = None
    descripcion: Optional[str] = None
class AreaOut(BaseModel):
    id_area: int
    nombre_area: str
    responsable: Optional[str]
    ubicacion: Optional[str]
    descripcion: Optional[str]
    class Config: from_attributes = True

# ---- EstadoReporte ----
class EstadoReporteCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    color: Optional[str] = None
    orden: Optional[int] = None
    es_final: Optional[bool] = False
class EstadoReporteUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    color: Optional[str] = None
    orden: Optional[int] = None
    es_final: Optional[bool] = None
class EstadoReporteOut(BaseModel):
    id_estado: int
    nombre: str
    descripcion: Optional[str]
    color: Optional[str]
    orden: Optional[int]
    es_final: bool
    class Config: from_attributes = True

# ---- Reporte ----
class ReporteCreate(BaseModel):
    titulo: str = Field(min_length=3)
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None
    id_categoria: Optional[int] = None
    id_area: Optional[int] = None
    id_estado: Optional[int] = None
class ReporteUpdate(BaseModel):
    titulo: Optional[str] = Field(default=None, min_length=3)
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None
    id_categoria: Optional[int] = None
    id_area: Optional[int] = None
    id_estado: Optional[int] = None
class ReporteOut(BaseModel):
    id_reporte: int
    id_usuario: int
    titulo: str
    descripcion: Optional[str]
    ubicacion: Optional[str]
    id_categoria: Optional[int]
    id_area: Optional[int]
    id_estado: Optional[int]
    creado_en: datetime
    class Config: from_attributes = True

# ---- ArchivoAdjunto ----
class ArchivoAdjuntoCreate(BaseModel):
    id_reporte: int
    nombre_archivo: str
    tipo: Optional[str] = None
    url: str
class ArchivoAdjuntoUpdate(BaseModel):
    nombre_archivo: Optional[str] = None
    tipo: Optional[str] = None
    url: Optional[str] = None
class ArchivoAdjuntoOut(BaseModel):
    id_archivo: int
    id_reporte: int
    nombre_archivo: str
    tipo: Optional[str]
    url: str
    class Config: from_attributes = True

# ---- Comentario ----
class ComentarioCreate(BaseModel):
    id_reporte: int
    contenido: str
class ComentarioUpdate(BaseModel):
    contenido: Optional[str] = None
class ComentarioOut(BaseModel):
    id_comentario: int
    id_reporte: int
    id_usuario: int
    contenido: str
    fecha: datetime
    class Config: from_attributes = True

# ---- Puntuacion ----
class PuntuacionCreate(BaseModel):
    id_reporte: int
    valor: int = Field(ge=1, le=5)
class PuntuacionUpdate(BaseModel):
    valor: Optional[int] = Field(default=None, ge=1, le=5)
class PuntuacionOut(BaseModel):
    id_puntuacion: int
    id_reporte: int
    id_usuario: int
    valor: int
    fecha: datetime
    class Config: from_attributes = True

# ---- Etiqueta ----
class EtiquetaCreate(BaseModel):
    nombre: str
    color: Optional[str] = None
class EtiquetaUpdate(BaseModel):
    nombre: Optional[str] = None
    color: Optional[str] = None
class EtiquetaOut(BaseModel):
    id_etiqueta: int
    nombre: str
    color: Optional[str]
    class Config: from_attributes = True
