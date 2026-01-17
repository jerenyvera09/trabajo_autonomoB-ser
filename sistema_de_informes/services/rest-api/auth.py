from __future__ import annotations

import os
import secrets
from typing import Any, Dict, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Header, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from db import get_db
from entities.rol import Rol
from entities.usuario import Usuario
from schemas.schemas import LoginIn, TokenOut, UsuarioCreate


router = APIRouter(prefix="/auth", tags=["Auth"])

# Pilar 1: La autenticación real vive en el Auth Service.
# Este router actúa como "API Gateway" para no duplicar credenciales en REST.
AUTH_SERVICE_URL = (os.getenv("AUTH_SERVICE_URL") or "http://auth-service:8001").rstrip("/")

# Solo para crear/actualizar un usuario de perfil local (P1) sin almacenar contraseña real.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def _sync_local_user(db: Session, nombre: str, email: str, id_rol: Optional[int] = None) -> None:
    existing = db.query(Usuario).filter(Usuario.email == email).first()

    # Validación de integridad: si se especifica rol, debe existir
    if id_rol is not None and not db.query(Rol).get(id_rol):
        raise HTTPException(status_code=400, detail="Rol no existe")

    if existing:
        if nombre and existing.nombre != nombre:
            existing.nombre = nombre
        if id_rol is not None and existing.id_rol != id_rol:
            existing.id_rol = id_rol
        db.commit()
        return

    dummy_password = pwd_context.hash(secrets.token_hex(16))
    user = Usuario(nombre=nombre, email=email, password_hash=dummy_password, estado="ACTIVO", id_rol=id_rol)
    db.add(user)
    db.commit()


def _raise_proxy_error(status_code: int, data: Any) -> None:
    detail = None
    if isinstance(data, dict):
        detail = data.get("detail") or data.get("message")
    raise HTTPException(status_code=status_code, detail=detail or "Error en Auth Service")


@router.post("/register", response_model=dict, status_code=201)
def register(payload: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra el usuario en Auth Service y sincroniza un perfil local en REST."""

    body = {"nombre": payload.nombre, "email": str(payload.email), "password": payload.password}
    try:
        with httpx.Client(timeout=10.0) as client:
            r = client.post(f"{AUTH_SERVICE_URL}/auth/register", json=body)
            data = r.json() if r.content else {}
            if r.status_code >= 400:
                _raise_proxy_error(r.status_code, data)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Auth Service no disponible: {e}")

    _sync_local_user(db=db, nombre=payload.nombre, email=str(payload.email), id_rol=payload.id_rol)
    return {"status": "ok", "email": str(payload.email)}


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    """Login contra Auth Service. Devuelve access+refresh tokens (Pilar 1)."""

    body = {"email": str(payload.email), "password": payload.password}
    try:
        with httpx.Client(timeout=10.0) as client:
            r = client.post(f"{AUTH_SERVICE_URL}/auth/login", json=body)
            data = r.json() if r.content else {}
            if r.status_code >= 400:
                _raise_proxy_error(r.status_code, data)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Auth Service no disponible: {e}")

    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    if not access_token:
        raise HTTPException(status_code=500, detail="Respuesta inválida de Auth Service")

    # Intentar obtener /me para sincronizar nombre/email si está disponible
    try:
        with httpx.Client(timeout=10.0) as client:
            me_r = client.get(f"{AUTH_SERVICE_URL}/auth/me", headers={"Authorization": f"Bearer {access_token}"})
            me_data = me_r.json() if me_r.content else {}
            if me_r.status_code < 400 and isinstance(me_data, dict):
                nombre = str(me_data.get("nombre") or me_data.get("name") or (payload.email.split("@", 1)[0]))
                _sync_local_user(db=db, nombre=nombre, email=str(payload.email), id_rol=None)
            else:
                _sync_local_user(db=db, nombre=(payload.email.split("@", 1)[0]), email=str(payload.email), id_rol=None)
    except Exception:
        _sync_local_user(db=db, nombre=(payload.email.split("@", 1)[0]), email=str(payload.email), id_rol=None)

    return TokenOut(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout", response_model=dict)
def logout(
    refresh_token: Optional[str] = None,
    authorization: Optional[str] = Header(None),
):
    body: Dict[str, Any] = {"refresh_token": refresh_token}
    headers: Dict[str, str] = {}
    if authorization:
        headers["Authorization"] = authorization
    try:
        with httpx.Client(timeout=10.0) as client:
            r = client.post(f"{AUTH_SERVICE_URL}/auth/logout", json=body, headers=headers)
            data = r.json() if r.content else {}
            if r.status_code >= 400:
                _raise_proxy_error(r.status_code, data)
            return data if isinstance(data, dict) else {"status": "ok"}
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Auth Service no disponible: {e}")


@router.post("/refresh", response_model=TokenOut)
def refresh(refresh_token: str):
    body = {"refresh_token": refresh_token}
    try:
        with httpx.Client(timeout=10.0) as client:
            r = client.post(f"{AUTH_SERVICE_URL}/auth/refresh", json=body)
            data = r.json() if r.content else {}
            if r.status_code >= 400:
                _raise_proxy_error(r.status_code, data)
            return TokenOut(access_token=data.get("access_token"), refresh_token=data.get("refresh_token"))
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Auth Service no disponible: {e}")


@router.get("/me", response_model=dict)
def me(authorization: Optional[str] = Header(None)):
    headers: Dict[str, str] = {}
    if authorization:
        headers["Authorization"] = authorization
    try:
        with httpx.Client(timeout=10.0) as client:
            r = client.get(f"{AUTH_SERVICE_URL}/auth/me", headers=headers)
            data = r.json() if r.content else {}
            if r.status_code >= 400:
                _raise_proxy_error(r.status_code, data)
            return data if isinstance(data, dict) else {"status": "ok"}
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Auth Service no disponible: {e}")
