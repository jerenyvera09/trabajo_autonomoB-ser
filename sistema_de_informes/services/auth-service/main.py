from fastapi import FastAPI, Depends, HTTPException, status, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import Optional

from db import Base, engine, get_db
from models import Usuario, RefreshToken, RevokedToken
from schemas import RegisterIn, LoginIn, TokenPairOut, AccessTokenOut, UserOut, RefreshIn, LogoutIn, ValidateOut
from security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token, rate_limiter

load_dotenv()

app = FastAPI(title="Auth Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)) -> Usuario:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Falta token")
    token = authorization.split(" ", 1)[1]
    try:
        claims = decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    if claims.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token no es de acceso")
    # Blacklist: jti en revoked_tokens
    jti = claims.get("jti")
    if jti and db.query(RevokedToken).filter(RevokedToken.jti == jti).first():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revocado")
    user_id = int(claims.get("sub"))
    user = db.query(Usuario).get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    return user


@app.post("/auth/register", response_model=UserOut, status_code=201)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    user = Usuario(
        nombre=payload.nombre,
        email=payload.email,
        password_hash=hash_password(payload.password),
        estado="ACTIVO",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut(id_usuario=user.id_usuario, nombre=user.nombre, email=user.email, estado=user.estado)


@app.post("/auth/login", response_model=TokenPairOut)
def login(payload: LoginIn, request: Request, db: Session = Depends(get_db), x_forwarded_for: Optional[str] = Header(None)):
    # Rate limiting por IP y email usando IP real
    ip = None
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    if not ip and request.client:
        ip = request.client.host
    ip = ip or "127.0.0.1"

    key_email = f"email:{payload.email}"
    key_ip = f"ip:{ip}"
    if not rate_limiter.allow(key_email) or not rate_limiter.allow(key_ip):
        raise HTTPException(status_code=429, detail="Demasiados intentos de login. Intente luego.")

    user = db.query(Usuario).filter(Usuario.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    access_token, access_jti, _ = create_access_token(str(user.id_usuario), {"email": user.email})
    refresh_token, refresh_jti, refresh_exp = create_refresh_token(str(user.id_usuario))

    db.add(RefreshToken(user_id=user.id_usuario, token=refresh_token, jti=refresh_jti, expires_at=refresh_exp))
    db.commit()

    return TokenPairOut(access_token=access_token, refresh_token=refresh_token)


@app.post("/auth/logout", response_model=dict)
def logout(payload: LogoutIn, user: Usuario = Depends(get_current_user), db: Session = Depends(get_db), authorization: str = Header(None)):
    # Revocar el access token actual
    token = authorization.split(" ", 1)[1]
    try:
        claims = decode_token(token)
        jti = claims.get("jti")
    except Exception:
        raise HTTPException(status_code=400, detail="Token inválido")
    if jti:
        # Idempotencia: no insertar si ya existe revocado
        existing = db.query(RevokedToken).filter(RevokedToken.jti == jti).first()
        if not existing:
            db.add(RevokedToken(jti=jti, token=token, reason="logout"))

    # Si se envía refresh_token, revocarlo también
    if payload.refresh_token:
        try:
            r_claims = decode_token(payload.refresh_token)
        except Exception:
            raise HTTPException(status_code=400, detail="Refresh token inválido")
        if r_claims.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Refresh token inválido")
        rt = db.query(RefreshToken).filter(RefreshToken.jti == r_claims.get("jti")).first()
        if rt:
            rt.revoked = True
    db.commit()
    return {"status": "ok"}


@app.post("/auth/refresh", response_model=TokenPairOut)
def refresh(payload: RefreshIn, db: Session = Depends(get_db)):
    try:
        claims = decode_token(payload.refresh_token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido")
    if claims.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido")

    # Debe existir y no estar revocado
    rt = db.query(RefreshToken).filter(RefreshToken.jti == claims.get("jti")).first()
    if not rt or rt.revoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revocado")

    user_id = int(claims.get("sub"))
    user = db.query(Usuario).get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

    # Rotación de refresh: revocar el actual y emitir nuevo
    rt.revoked = True

    access_token, access_jti, _ = create_access_token(str(user.id_usuario), {"email": user.email})
    new_refresh_token, new_refresh_jti, new_refresh_exp = create_refresh_token(str(user.id_usuario))
    db.add(RefreshToken(user_id=user.id_usuario, token=new_refresh_token, jti=new_refresh_jti, expires_at=new_refresh_exp))
    db.commit()

    return TokenPairOut(access_token=access_token, refresh_token=new_refresh_token)


@app.get("/auth/me", response_model=UserOut)
def me(user: Usuario = Depends(get_current_user)):
    return UserOut(id_usuario=user.id_usuario, nombre=user.nombre, email=user.email, estado=user.estado)


@app.get("/auth/validate", response_model=ValidateOut)
def validate(token: Optional[str] = None, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    t = token
    if not t and authorization and authorization.lower().startswith("bearer "):
        t = authorization.split(" ", 1)[1]
    if not t:
        return ValidateOut(valid=False, reason="Falta token")
    try:
        claims = decode_token(t)
    except Exception:
        return ValidateOut(valid=False, reason="Token inválido")
    # Verificar blacklist si es access
    if claims.get("type") == "access":
        jti = claims.get("jti")
        if jti and db.query(RevokedToken).filter(RevokedToken.jti == jti).first():
            return ValidateOut(valid=False, reason="Token revocado")
    return ValidateOut(valid=True, claims=claims)


@app.get("/")
def root():
    return {"status": "ok", "service": "auth-service"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "auth-service"}
