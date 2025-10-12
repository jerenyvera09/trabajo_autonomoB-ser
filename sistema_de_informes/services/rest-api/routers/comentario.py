from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from entities.comentario import Comentario
from schemas.schemas import ComentarioCreate, ComentarioOut, ComentarioUpdate
from deps import Auth
from entities.reporte import Reporte

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])

@router.get("", response_model=list[ComentarioOut])
def listar(db: Session = Depends(get_db), user=Depends(Auth)):
    return db.query(Comentario).all()

@router.post("", response_model=ComentarioOut, status_code=201)
def crear(payload: ComentarioCreate, db: Session = Depends(get_db), user=Depends(Auth)):
    if not db.query(Reporte).get(payload.id_reporte):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reporte no existe")
    obj = Comentario(
        id_usuario=user.id_usuario,
        id_reporte=payload.id_reporte,
        contenido=payload.contenido
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/{id_comentario}", response_model=ComentarioOut)
def obtener(id_comentario: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Comentario).get(id_comentario)
    if not obj:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return obj

@router.put("/{id_comentario}", response_model=ComentarioOut)
def actualizar(id_comentario: int, payload: ComentarioUpdate, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Comentario).get(id_comentario)
    if not obj:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{id_comentario}", status_code=204)
def eliminar(id_comentario: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Comentario).get(id_comentario)
    if not obj:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    db.delete(obj); db.commit()
    return None
