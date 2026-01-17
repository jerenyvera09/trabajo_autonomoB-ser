from datetime import datetime
from typing import Any, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine, SessionLocal
from auth import router as auth_router
from routers.usuario import router as usuarios_router
from routers.rol import router as roles_router
from routers.reporte import router as reportes_router
from routers.categoria import router as categorias_router
from routers.archivo_adjunto import router as archivos_router
from routers.area import router as areas_router
from routers.estado_reporte import router as estados_router
from routers.comentario import router as comentarios_router
from routers.puntuacion import router as puntuaciones_router
from routers.etiqueta import router as etiquetas_router
from routers.pdf import router as pdf_router
from routers.integrations import router as integrations_router
from entities.reporte import Reporte
from entities.estado_reporte import EstadoReporte
from entities.categoria import Categoria
from entities.area import Area
from entities.rol import Rol
from entities.usuario import Usuario
from entities.comentario import Comentario
from entities.puntuacion import Puntuacion
from entities.archivo_adjunto import ArchivoAdjunto
from entities.etiqueta import Etiqueta
from deps import start_revoked_sync

app = FastAPI(title="REST API - Semana 4 (FastAPI)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def _startup_revoked_sync():
    # Sincronización periódica de tokens revocados (blacklist) desde auth-service.
    start_revoked_sync()

def to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


def serialize_report(reporte: Reporte, estados_lookup: dict[int | None, str]) -> dict[str, Any]:
    return {
        "id": reporte.id_reporte,
        "title": reporte.titulo,
        "description": reporte.descripcion or "",
        "status": estados_lookup.get(reporte.id_estado, "Sin estado"),
        "priority": "Media",
        "location": reporte.ubicacion or "",
        "created_at": to_iso(reporte.creado_en),
        "category_id": reporte.id_categoria,
        "user_id": reporte.id_usuario,
        "area_id": reporte.id_area,
        "state_id": reporte.id_estado,
    }


def serialize_categoria(categoria: Categoria) -> dict[str, Any]:
    return {
        "id": categoria.id_categoria,
        "name": categoria.nombre,
        "description": categoria.descripcion,
        "priority": categoria.prioridad,
        "status": categoria.estado,
    }


def serialize_area(area: Area) -> dict[str, Any]:
    return {
        "id": area.id_area,
        "name": area.nombre_area,
        "location": area.ubicacion,
        "responsable": area.responsable,
        "description": area.descripcion,
    }


def serialize_estado(estado: EstadoReporte) -> dict[str, Any]:
    return {
        "id": estado.id_estado,
        "name": estado.nombre,
        "description": estado.descripcion,
        "color": estado.color,
        "order": estado.orden,
        "final": estado.es_final,
    }


def serialize_rol(rol: Rol) -> dict[str, Any]:
    return {
        "id": rol.id_rol,
        "name": rol.nombre_rol,
        "description": rol.descripcion,
        "permissions": rol.permisos,
    }


def serialize_usuario(usuario: Usuario) -> dict[str, Any]:
    return {
        "id": usuario.id_usuario,
        "name": usuario.nombre,
        "email": usuario.email,
        "status": usuario.estado,
        "role_id": usuario.id_rol,
    }


def serialize_comentario(comentario: Comentario) -> dict[str, Any]:
    return {
        "id": comentario.id_comentario,
        "report_id": comentario.id_reporte,
        "user_id": comentario.id_usuario,
        "content": comentario.contenido,
        "date": to_iso(comentario.fecha),
    }


def serialize_puntuacion(puntuacion: Puntuacion) -> dict[str, Any]:
    return {
        "id": puntuacion.id_puntuacion,
        "report_id": puntuacion.id_reporte,
        "user_id": puntuacion.id_usuario,
        "value": puntuacion.valor,
        "date": to_iso(puntuacion.fecha),
    }


def serialize_archivo(archivo: ArchivoAdjunto) -> dict[str, Any]:
    return {
        "id": archivo.id_archivo,
        "report_id": archivo.id_reporte,
        "name": archivo.nombre_archivo,
        "type": archivo.tipo,
        "url": archivo.url,
    }


def serialize_etiqueta(etiqueta: Etiqueta) -> dict[str, Any]:
    return {
        "id": etiqueta.id_etiqueta,
        "name": etiqueta.nombre,
        "color": etiqueta.color,
    }

@app.get("/")
def root():
    return {"status": "ok", "service": "REST API"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "REST API"}

@app.get("/api/v1/reports")
def get_reports():
    with SessionLocal() as session:
        estados = {
            estado.id_estado: estado.nombre
            for estado in session.query(EstadoReporte).all()
        }
        reportes: List[Reporte] = (
            session.query(Reporte)
            .order_by(Reporte.creado_en.desc())
            .all()
        )
        return [serialize_report(reporte, estados) for reporte in reportes]


@app.get("/api/v1/categories")
def get_categories():
    with SessionLocal() as session:
        categorias = session.query(Categoria).order_by(Categoria.id_categoria).all()
        return [serialize_categoria(categoria) for categoria in categorias]


@app.get("/api/v1/areas")
def get_areas():
    with SessionLocal() as session:
        areas = session.query(Area).order_by(Area.id_area).all()
        return [serialize_area(area) for area in areas]


@app.get("/api/v1/states")
def get_states():
    with SessionLocal() as session:
        estados = session.query(EstadoReporte).order_by(EstadoReporte.orden, EstadoReporte.id_estado).all()
        return [serialize_estado(estado) for estado in estados]


@app.get("/api/v1/roles")
def get_roles():
    with SessionLocal() as session:
        roles = session.query(Rol).order_by(Rol.id_rol).all()
        return [serialize_rol(rol) for rol in roles]


@app.get("/api/v1/users")
def get_users():
    with SessionLocal() as session:
        usuarios = session.query(Usuario).order_by(Usuario.id_usuario).all()
        return [serialize_usuario(usuario) for usuario in usuarios]


@app.get("/api/v1/comments")
def get_comments():
    with SessionLocal() as session:
        comentarios = session.query(Comentario).order_by(Comentario.fecha.desc()).all()
        return [serialize_comentario(comentario) for comentario in comentarios]


@app.get("/api/v1/ratings")
def get_ratings():
    with SessionLocal() as session:
        puntuaciones = session.query(Puntuacion).order_by(Puntuacion.fecha.desc()).all()
        return [serialize_puntuacion(puntuacion) for puntuacion in puntuaciones]


@app.get("/api/v1/files")
def get_files():
    with SessionLocal() as session:
        archivos = session.query(ArchivoAdjunto).order_by(ArchivoAdjunto.id_archivo).all()
        return [serialize_archivo(archivo) for archivo in archivos]


@app.get("/api/v1/attachments")
def get_attachments():
    return get_files()


@app.get("/api/v1/tags")
def get_tags():
    with SessionLocal() as session:
        etiquetas = session.query(Etiqueta).order_by(Etiqueta.id_etiqueta).all()
        return [serialize_etiqueta(etiqueta) for etiqueta in etiquetas]

# Routers
app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(roles_router)
app.include_router(reportes_router)
app.include_router(categorias_router)
app.include_router(archivos_router)
app.include_router(areas_router)
app.include_router(estados_router)
app.include_router(comentarios_router)
app.include_router(puntuaciones_router)
app.include_router(etiquetas_router)
app.include_router(pdf_router)
app.include_router(integrations_router)