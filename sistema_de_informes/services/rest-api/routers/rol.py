from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from entities.rol import Rol
from schemas.schemas import RolCreate, RolOut, RolUpdate
from deps import Auth
from entities.usuario import Usuario

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("", response_model=list[RolOut])
def listar(db: Session = Depends(get_db), user=Depends(Auth)):
    return db.query(Rol).all()

@router.post("", response_model=RolOut, status_code=201)
def crear(payload: RolCreate, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = Rol(**payload.model_dict())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/{id_rol}", response_model=RolOut)
def obtener(id_rol: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Rol).get(id_rol)
    if not obj:
        raise HTTPException(status_code=404, detail="Roles no encontrado")
    return obj

@router.put("/{id_rol}", response_model=RolOut)
def actualizar(id_rol: int, payload: RolUpdate, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Rol).get(id_rol)
    if not obj:
        raise HTTPException(status_code=404, detail="Roles no encontrado")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{id_rol}", status_code=204)
def eliminar(id_rol: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Rol).get(id_rol)
    if not obj:
        raise HTTPException(status_code=404, detail="Roles no encontrado")
    if db.query(Usuario).filter(Usuario.id_rol == id_rol).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se puede eliminar el rol: existen usuarios asociados")
    db.delete(obj); db.commit()
    return None
