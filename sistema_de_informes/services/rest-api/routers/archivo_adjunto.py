from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from entities.archivo_adjunto import ArchivoAdjunto
from schemas.schemas import ArchivoAdjuntoCreate, ArchivoAdjuntoOut, ArchivoAdjuntoUpdate
from deps import Auth
from entities.reporte import Reporte

router = APIRouter(prefix="/archivos", tags=["ArchivosAdjuntos"])

@router.get("", response_model=list[ArchivoAdjuntoOut])
def listar(db: Session = Depends(get_db), user=Depends(Auth)):
    return db.query(ArchivoAdjunto).all()

@router.post("", response_model=ArchivoAdjuntoOut, status_code=201)
def crear(payload: ArchivoAdjuntoCreate, db: Session = Depends(get_db), user=Depends(Auth)):
    if not db.query(Reporte).get(payload.id_reporte):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reporte no existe")
    obj = ArchivoAdjunto(**payload.model_dict())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/{id_archivo}", response_model=ArchivoAdjuntoOut)
def obtener(id_archivo: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(ArchivoAdjunto).get(id_archivo)
    if not obj:
        raise HTTPException(status_code=404, detail="ArchivosAdjuntos no encontrado")
    return obj

@router.put("/{id_archivo}", response_model=ArchivoAdjuntoOut)
def actualizar(id_archivo: int, payload: ArchivoAdjuntoUpdate, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(ArchivoAdjunto).get(id_archivo)
    if not obj:
        raise HTTPException(status_code=404, detail="ArchivosAdjuntos no encontrado")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{id_archivo}", status_code=204)
def eliminar(id_archivo: int, db: Session = Depends(get_db), user=Depends(Auth)):
    obj = db.query(ArchivoAdjunto).get(id_archivo)
    if not obj:
        raise HTTPException(status_code=404, detail="ArchivosAdjuntos no encontrado")
    db.delete(obj); db.commit()
    return None
