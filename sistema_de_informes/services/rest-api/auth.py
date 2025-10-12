from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from db import get_db
from entities.usuario import Usuario
from schemas.schemas import UsuarioCreate, LoginIn, TokenOut
import os
from entities.rol import Rol

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-change-this")
ALGORITHM = os.getenv("JWT_ALG", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8

router = APIRouter(prefix="/auth", tags=["Auth"])

def hash_password(p: str) -> str: return pwd_context.hash(p)
def verify_password(p: str, h: str) -> bool: return pwd_context.verify(p, h)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=dict, status_code=201)
def register(payload: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    # Validación de integridad: si se especifica rol, debe existir
    if payload.id_rol is not None and not db.query(Rol).get(payload.id_rol):
        raise HTTPException(status_code=400, detail="Rol no existe")
    user = Usuario(
        nombre=payload.nombre,
        email=payload.email,
        password_hash=hash_password(payload.password),
        estado="ACTIVO",
        id_rol=payload.id_rol
    )
    db.add(user); db.commit(); db.refresh(user)
    return {"id_usuario": user.id_usuario, "email": user.email}

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    token = create_access_token({"sub": str(user.id_usuario), "email": user.email})
    return TokenOut(access_token=token)
