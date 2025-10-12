from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from entities.usuario import Usuario
from schemas.schemas import UsuarioOut, UsuarioUpdate
from deps import Auth
from entities.rol import Rol
from entities.reporte import Reporte
from entities.comentario import Comentario
from entities.puntuacion import Puntuacion

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("", response_model=list[UsuarioOut])
def listar(db: Session = Depends(get_db), user=Depends(Auth)):
    return db.query(Usuario).all()

@router.get("/{id_usuario}", response_model=UsuarioOut)
def obtener(id_usuario: int, db: Session = Depends(get_db), user=Depends(Auth)):
    u = db.query(Usuario).get(id_usuario)
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return u

@router.put("/{id_usuario}", response_model=UsuarioOut)
def actualizar(id_usuario: int, payload: UsuarioUpdate, db: Session = Depends(get_db), user=Depends(Auth)):
    u = db.query(Usuario).get(id_usuario)
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Validar rol si se intenta cambiar
    if payload.id_rol is not None and not db.query(Rol).get(payload.id_rol):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rol no existe")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(u, k, v)
    db.commit(); db.refresh(u)
    return u

@router.delete("/{id_usuario}", status_code=204)
def eliminar(id_usuario: int, db: Session = Depends(get_db), user=Depends(Auth)):
    u = db.query(Usuario).get(id_usuario)
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Impedir borrado si tiene entidades relacionadas
    if db.query(Reporte).filter(Reporte.id_usuario == id_usuario).first() or \
       db.query(Comentario).filter(Comentario.id_usuario == id_usuario).first() or \
       db.query(Puntuacion).filter(Puntuacion.id_usuario == id_usuario).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se puede eliminar el usuario: existen registros relacionados")
    db.delete(u); db.commit()
    return None
