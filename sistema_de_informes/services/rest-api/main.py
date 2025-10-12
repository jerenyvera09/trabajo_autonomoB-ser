from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine
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

app = FastAPI(title="REST API - Semana 4 (FastAPI)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "ok", "service": "rest-api"}

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
