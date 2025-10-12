from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from db import get_db
from entities.usuario import Usuario
import os

SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-change-this")
ALGORITHM = os.getenv("JWT_ALG", "HS256")

def Auth(dep_db: Session = Depends(get_db), authorization: str | None = None) -> Usuario:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Falta token Bearer")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    uid = int(payload.get("sub", 0))
    user = dep_db.query(Usuario).get(uid)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user
