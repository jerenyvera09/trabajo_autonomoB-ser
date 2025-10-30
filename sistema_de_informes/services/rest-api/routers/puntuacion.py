from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from entities.puntuacion import Puntuacion
from schemas.schemas import PuntuacionCreate, PuntuacionOut, PuntuacionUpdate
from deps import Auth
from entities.reporte import Reporte
from ws_notifier import notify_rating_added  # 🔥 WebSocket notifier

router = APIRouter(prefix="/puntuaciones", tags=["Puntuaciones"])

@router.get("", response_model=list[PuntuacionOut])
def listar(db: Session = Depends(get_db), user=Depends(Auth)):
    return db.query(Puntuacion).all()

@router.post("", response_model=PuntuacionOut, status_code=201)
async def crear(payload: PuntuacionCreate, db: Session = Depends(get_db), user=Depends(Auth)):
    if not db.query(Reporte).get(payload.id_reporte):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reporte no existe")
    obj = Puntuacion(
        id_usuario=user.id_usuario,
        id_reporte=payload.id_reporte,
        valor=payload.valor
    )
    db.add(obj); db.commit(); db.refresh(obj)
    
    # 🔥 NOTIFICAR AL WEBSOCKET
    await notify_rating_added(obj.id_reporte, obj.valor)
    
    return obj

@router.get("/{id_puntuacion}", response_model=PuntuacionOut)
def obtener(id_puntuacion: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Puntuacion).get(id_puntuacion)
    if not obj:
        raise HTTPException(status_code=404, detail="Puntuación no encontrada")
    return obj

@router.put("/{id_puntuacion}", response_model=PuntuacionOut)
def actualizar(id_puntuacion: int, payload: PuntuacionUpdate, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Puntuacion).get(id_puntuacion)
    if not obj:
        raise HTTPException(status_code=404, detail="Puntuación no encontrada")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{id_puntuacion}", status_code=204)
def eliminar(id_puntuacion: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Puntuacion).get(id_puntuacion)
    if not obj:
        raise HTTPException(status_code=404, detail="Puntuación no encontrada")
    db.delete(obj); db.commit()
    return None
