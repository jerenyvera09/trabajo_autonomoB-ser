from fastapi import Depends, HTTPException, status, Header
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from db import get_db
from entities.usuario import Usuario
import os

import threading
import time
from typing import Optional, Set

import httpx

SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-change-this")
ALGORITHM = os.getenv("JWT_ALG", "HS256")

AUTH_SERVICE_URL = (os.getenv("AUTH_SERVICE_URL") or "http://auth-service:8001").rstrip("/")
REVOKED_SYNC_SECONDS = int(os.getenv("REVOKED_SYNC_SECONDS", "30"))

_revoked_jtis: Set[str] = set()
_revoked_mu = threading.Lock()
_revoked_started = False


def _set_revoked(jtis: Set[str]) -> None:
    global _revoked_jtis
    with _revoked_mu:
        _revoked_jtis = set(jtis)


def is_revoked(jti: Optional[str]) -> bool:
    if not jti:
        return False
    with _revoked_mu:
        return jti in _revoked_jtis


def start_revoked_sync() -> None:
    """Sincroniza blacklist desde auth-service cada N segundos.

    Cumple: validación local (sin consultar auth-service en cada request).
    """

    global _revoked_started
    if _revoked_started:
        return
    _revoked_started = True

    def loop() -> None:
        while True:
            try:
                with httpx.Client(timeout=5.0) as client:
                    r = client.get(f"{AUTH_SERVICE_URL}/auth/revoked")
                    if r.status_code < 400:
                        data = r.json() if r.content else {}
                        jtis = data.get("jtis")
                        if isinstance(jtis, list):
                            cleaned = {str(x) for x in jtis if isinstance(x, str) and x}
                            _set_revoked(cleaned)
            except Exception:
                # Silencioso: no bloquea la app si auth-service cae
                pass
            time.sleep(max(5, REVOKED_SYNC_SECONDS))

    t = threading.Thread(target=loop, daemon=True)
    t.start()

def Auth(authorization: str | None = Header(None), dep_db: Session = Depends(get_db)) -> Usuario:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Falta token Bearer")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    # Blacklist local (sin llamada por request)
    jti = payload.get("jti")
    if isinstance(jti, str) and is_revoked(jti):
        raise HTTPException(status_code=401, detail="Token revocado")
    # Pilar 1: validación local por firma/exp.
    # Nota: el Auth Service emite `sub` como id de su propia DB, por lo que aquí
    # buscamos al usuario local por `email` (claim) cuando esté presente.
    email = payload.get("email")
    user = None
    if isinstance(email, str) and email:
        user = dep_db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        uid = int(payload.get("sub", 0) or 0)
        user = dep_db.query(Usuario).get(uid) if uid else None
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user
