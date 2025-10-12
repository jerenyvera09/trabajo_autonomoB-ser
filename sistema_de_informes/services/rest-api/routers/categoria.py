from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from entities.categoria import Categoria
from schemas.schemas import CategoriaCreate, CategoriaOut, CategoriaUpdate
from deps import Auth
from entities.reporte import Reporte

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get("", response_model=list[CategoriaOut])
def listar(db: Session = Depends(get_db), user=Depends(Auth)):
    return db.query(Categoria).all()

@router.post("", response_model=CategoriaOut, status_code=201)
def crear(payload: CategoriaCreate, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = Categoria(**payload.model_dict())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/{id_categoria}", response_model=CategoriaOut)
def obtener(id_categoria: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Categoria).get(id_categoria)
    if not obj:
        raise HTTPException(status_code=404, detail="Categorias no encontrado")
    return obj

@router.put("/{id_categoria}", response_model=CategoriaOut)
def actualizar(id_categoria: int, payload: CategoriaUpdate, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Categoria).get(id_categoria)
    if not obj:
        raise HTTPException(status_code=404, detail="Categorias no encontrado")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{id_categoria}", status_code=204)
def eliminar(id_categoria: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(Categoria).get(id_categoria)
    if not obj:
        raise HTTPException(status_code=404, detail="Categorias no encontrado")
    # No permitir borrar si hay reportes asociados
    if db.query(Reporte).filter(Reporte.id_categoria == id_categoria).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se puede eliminar la categoría: existen reportes asociados")
    db.delete(obj); db.commit()
    return None
