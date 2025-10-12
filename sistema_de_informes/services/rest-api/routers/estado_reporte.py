from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from entities.estado_reporte import EstadoReporte
from schemas.schemas import EstadoReporteCreate, EstadoReporteOut, EstadoReporteUpdate
from deps import Auth
from entities.reporte import Reporte

router = APIRouter(prefix="/estados-reporte", tags=["EstadosReporte"])

@router.get("", response_model=list[EstadoReporteOut])
def listar(db: Session = Depends(get_db), user=Depends(Auth)):
    return db.query(EstadoReporte).all()

@router.post("", response_model=EstadoReporteOut, status_code=201)
def crear(payload: EstadoReporteCreate, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = EstadoReporte(**payload.model_dict())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/{id_estado}", response_model=EstadoReporteOut)
def obtener(id_estado: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(EstadoReporte).get(id_estado)
    if not obj:
        raise HTTPException(status_code=404, detail="EstadosReporte no encontrado")
    return obj

@router.put("/{id_estado}", response_model=EstadoReporteOut)
def actualizar(id_estado: int, payload: EstadoReporteUpdate, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(EstadoReporte).get(id_estado)
    if not obj:
        raise HTTPException(status_code=404, detail="EstadosReporte no encontrado")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{id_estado}", status_code=204)
def eliminar(id_estado: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(EstadoReporte).get(id_estado)
    if not obj:
        raise HTTPException(status_code=404, detail="EstadosReporte no encontrado")
    if db.query(Reporte).filter(Reporte.id_estado == id_estado).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se puede eliminar el estado: existen reportes asociados")
    db.delete(obj); db.commit()
    return None
