from __future__ import annotations

import hmac
import hashlib
from typing import Optional


def compute_hmac_sha256(secret: str, body: bytes) -> str:
    mac = hmac.new(secret.encode("utf-8"), body, hashlib.sha256)
    return mac.hexdigest()


def _normalize_sig(sig: str) -> str:
    s = (sig or "").strip()
    # Soportar formato "sha256=<hex>" de forma opcional
    if s.lower().startswith("sha256="):
        return s.split("=", 1)[1].strip()
    return s


def verify_hmac_sha256(secret: str, body: bytes, signature_header: Optional[str]) -> bool:
    if not signature_header:
        return False
    expected = compute_hmac_sha256(secret, body)
    provided = _normalize_sig(signature_header)
    # Comparación en tiempo constante
    return hmac.compare_digest(expected, provided)
