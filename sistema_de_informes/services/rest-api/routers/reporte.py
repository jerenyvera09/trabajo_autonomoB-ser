from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from entities.reporte import Reporte
from schemas.schemas import ReporteCreate, ReporteOut, ReporteUpdate
from deps import Auth
from entities.categoria import Categoria
from entities.area import Area
from entities.estado_reporte import EstadoReporte
from ws_notifier import notify_new_report, notify_update_report  # 🔥 WebSocket notifier

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("", response_model=list[ReporteOut])
def listar(db: Session = Depends(get_db), user=Depends(Auth)):
    return db.query(Reporte).all()

@router.post("", response_model=ReporteOut, status_code=201)
async def crear(payload: ReporteCreate, db: Session = Depends(get_db), user=Depends(Auth)):
    # Validaciones de integridad referencial
    if payload.id_categoria is not None and not db.query(Categoria).get(payload.id_categoria):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria no existe")
    if payload.id_area is not None and not db.query(Area).get(payload.id_area):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Area no existe")
    if payload.id_estado is not None and not db.query(EstadoReporte).get(payload.id_estado):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Estado de reporte no existe")
    rep = Reporte(
        id_usuario=user.id_usuario,
        titulo=payload.titulo,
        descripcion=payload.descripcion,
        ubicacion=payload.ubicacion,
        id_categoria=payload.id_categoria,
        id_area=payload.id_area,
        id_estado=payload.id_estado
    )
    db.add(rep); db.commit(); db.refresh(rep)
    
    # 🔥 NOTIFICAR AL WEBSOCKET
    await notify_new_report(rep.id_reporte, rep.titulo)
    
    return rep

@router.get("/{id_reporte}", response_model=ReporteOut)
def obtener(id_reporte: int, db: Session = Depends(get_db), user=Depends(Auth)):
    rep = db.query(Reporte).get(id_reporte)
    if not rep:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return rep

@router.put("/{id_reporte}", response_model=ReporteOut)
async def actualizar(id_reporte: int, payload: ReporteUpdate, db: Session = Depends(get_db), user=Depends(Auth)):
    rep = db.query(Reporte).get(id_reporte)
    if not rep:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    # Validaciones de integridad referencial para campos enviados
    if payload.id_categoria is not None and not db.query(Categoria).get(payload.id_categoria):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria no existe")
    if payload.id_area is not None and not db.query(Area).get(payload.id_area):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Area no existe")
    if payload.id_estado is not None and not db.query(EstadoReporte).get(payload.id_estado):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Estado de reporte no existe")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(rep, k, v)
    db.commit(); db.refresh(rep)
    
    # 🔥 NOTIFICAR AL WEBSOCKET
    await notify_update_report(rep.id_reporte, rep.titulo)
    
    return rep

@router.delete("/{id_reporte}", status_code=204)
def eliminar(id_reporte: int, db: Session = Depends(get_db), user=Depends(Auth)):
    rep = db.query(Reporte).get(id_reporte)
    if not rep:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    db.delete(rep); db.commit()
    return None
