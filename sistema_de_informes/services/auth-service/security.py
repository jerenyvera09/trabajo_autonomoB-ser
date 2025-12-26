import os
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List
from jose import jwt, JWTError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

JWT_SECRET = os.getenv("JWT_SECRET", "please-change-this-secret")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "10080"))

RATE_LIMIT_LOGIN_ATTEMPTS = int(os.getenv("RATE_LIMIT_LOGIN_ATTEMPTS", "5"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

class RateLimiter:
    def __init__(self, max_attempts: int, window_seconds: int):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._store: Dict[str, List[float]] = {}

    def allow(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        attempts = [t for t in self._store.get(key, []) if t >= window_start]
        if len(attempts) >= self.max_attempts:
            self._store[key] = attempts
            return False
        attempts.append(now)
        self._store[key] = attempts
        return True

rate_limiter = RateLimiter(RATE_LIMIT_LOGIN_ATTEMPTS, RATE_LIMIT_WINDOW_SECONDS)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def _expiry(minutes: int) -> datetime:
    return datetime.utcnow() + timedelta(minutes=minutes)


def generate_jti() -> str:
    return uuid.uuid4().hex


def create_access_token(subject: str, extra_claims: dict | None = None) -> tuple[str, str, datetime]:
    jti = generate_jti()
    exp_dt = _expiry(ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "type": "access", "jti": jti, "exp": exp_dt}
    if extra_claims:
        payload.update(extra_claims)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
    return token, jti, exp_dt


def create_refresh_token(subject: str, extra_claims: dict | None = None) -> tuple[str, str, datetime]:
    jti = generate_jti()
    exp_dt = _expiry(REFRESH_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "type": "refresh", "jti": jti, "exp": exp_dt}
    if extra_claims:
        payload.update(extra_claims)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
    return token, jti, exp_dt


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except JWTError as e:
        raise e
