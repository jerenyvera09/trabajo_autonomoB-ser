from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from entities.area import Area
from schemas.schemas import AreaCreate, AreaOut, AreaUpdate
from deps import Auth
from entities.reporte import Reporte

router = APIRouter(prefix="/areas", tags=["Areas"])

@router.get("", response_model=list[AreaOut])
def listar(db: Session = Depends(get_db), user=Depends(Auth)):
    return db.query(Area).all()

@router.post("", response_model=AreaOut, status_code=201)
def crear(payload: AreaCreate, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = Area(**payload.model_dict())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/{id_area}", response_model=AreaOut)
def obtener(id_area: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Area).get(id_area)
    if not obj:
        raise HTTPException(status_code=404, detail="Areas no encontrado")
    return obj

@router.put("/{id_area}", response_model=AreaOut)
def actualizar(id_area: int, payload: AreaUpdate, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Area).get(id_area)
    if not obj:
        raise HTTPException(status_code=404, detail="Areas no encontrado")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{id_area}", status_code=204)
def eliminar(id_area: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Area).get(id_area)
    if not obj:
        raise HTTPException(status_code=404, detail="Areas no encontrado")
    if db.query(Reporte).filter(Reporte.id_area == id_area).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se puede eliminar el área: existen reportes asociados")
    db.delete(obj); db.commit()
    return None
