from __future__ import annotations

from typing import Any, Dict

from domain.models import utc_now_iso


def normalize_webhook(provider: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Convierte cualquier webhook a un formato común.

    Formato común (Semana 2):
    {
      "event": "payment.success",
      "paymentId": "...",
      "provider": "mock",
      "timestamp": "..."
    }

    Para demo local, aceptamos payloads sencillos.
    """

    provider = (provider or "unknown").lower()

    # Si ya viene normalizado, respetarlo.
    if all(k in payload for k in ("event", "paymentId")):
        return {
            "event": str(payload["event"]),
            "paymentId": str(payload["paymentId"]),
            "provider": provider,
            "timestamp": str(payload.get("timestamp") or utc_now_iso()),
        }

    # Mock: {"type": "payment.success", "paymentId": "..."}
    if provider == "mock":
        event = str(payload.get("type") or payload.get("event") or "payment.unknown")
        payment_id = str(payload.get("paymentId") or payload.get("payment_id") or payload.get("id") or "")
        return {
            "event": event,
            "paymentId": payment_id,
            "provider": provider,
            "timestamp": utc_now_iso(),
        }

    # Stripe (demo): soportar el formato típico {"type": "payment_intent.succeeded", "data": {"object": {"id": "pi_..."}}}
    if provider == "stripe":
        raw_type = str(payload.get("type") or payload.get("event") or "")
        # Normalizar a contrato del curso
        mapping = {
            "payment_intent.succeeded": "payment.success",
            "checkout.session.completed": "payment.success",
            "payment_intent.payment_failed": "payment.failed",
            "payment_intent.processing": "payment.pending",
        }
        event = mapping.get(raw_type, raw_type or "payment.unknown")

        payment_id = str(payload.get("paymentId") or payload.get("payment_id") or "")
        data = payload.get("data")
        if not payment_id and isinstance(data, dict):
            obj = data.get("object")
            if isinstance(obj, dict):
                payment_id = str(obj.get("id") or "")

        return {
            "event": event,
            "paymentId": payment_id,
            "provider": provider,
            "timestamp": str(payload.get("created") or utc_now_iso()),
        }

    # Partners: permitir {"eventName": "...", "payment": {"id": "..."}}
    event = str(payload.get("eventName") or payload.get("type") or "payment.unknown")
    payment_id = ""
    if isinstance(payload.get("payment"), dict):
        payment_id = str(payload["payment"].get("id") or "")
    if not payment_id:
        payment_id = str(payload.get("paymentId") or payload.get("payment_id") or "")

    return {
        "event": event,
        "paymentId": payment_id,
        "provider": provider,
        "timestamp": utc_now_iso(),
    }
