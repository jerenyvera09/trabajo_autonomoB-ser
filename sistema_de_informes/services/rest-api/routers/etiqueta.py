from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from entities.etiqueta import Etiqueta
from schemas.schemas import EtiquetaCreate, EtiquetaOut, EtiquetaUpdate
from deps import Auth

router = APIRouter(prefix="/etiquetas", tags=["Etiquetas"])

@router.get("", response_model=list[EtiquetaOut])
def listar(db: Session = Depends(get_db), user=Depends(Auth)):
    return db.query(Etiqueta).all()

@router.post("", response_model=EtiquetaOut, status_code=201)
def crear(payload: EtiquetaCreate, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = Etiqueta(**payload.model_dict())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/{id_etiqueta}", response_model=EtiquetaOut)
def obtener(id_etiqueta: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Etiqueta).get(id_etiqueta)
    if not obj:
        raise HTTPException(status_code=404, detail="Etiquetas no encontrado")
    return obj

@router.put("/{id_etiqueta}", response_model=EtiquetaOut)
def actualizar(id_etiqueta: int, payload: EtiquetaUpdate, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Etiqueta).get(id_etiqueta)
    if not obj:
        raise HTTPException(status_code=404, detail="Etiquetas no encontrado")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{id_etiqueta}", status_code=204)
def eliminar(id_etiqueta: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Etiqueta).get(id_etiqueta)
    if not obj:
        raise HTTPException(status_code=404, detail="Etiquetas no encontrado")
    db.delete(obj); db.commit()
    return None
