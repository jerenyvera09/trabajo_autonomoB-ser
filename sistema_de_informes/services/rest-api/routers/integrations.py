from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from typing import Any, Optional

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from ws_notifier import notify_websocket

router = APIRouter(prefix="/api/v1/integrations", tags=["Integrations"])


def _require_internal_token(x_internal_token: Optional[str]) -> None:
    expected = (os.getenv("INTERNAL_WEBHOOK_TOKEN") or "").strip()
    if not expected:
        raise HTTPException(
            status_code=500,
            detail="INTERNAL_WEBHOOK_TOKEN no está configurado en el servicio REST",
        )

    provided = (x_internal_token or "").strip()
    if provided != expected:
        raise HTTPException(status_code=401, detail="Token interno inválido")


class ActivateIn(BaseModel):
    event: str
    paymentId: str | None = None
    partnerId: str | None = None
    amount: float | None = None
    currency: str | None = None
    extra: dict[str, Any] | None = None


@router.post("/activate")
async def activate(
    payload: ActivateIn,
    x_internal_token: Optional[str] = Header(default=None, alias="X-Internal-Token"),
):
    """Punto de integración para n8n (Event Bus).

    - Representa la "activación" de la lógica de negocio ante un evento externo.
    - Notifica por WebSocket a los clientes conectados.

    Nota: Se protege con token interno para evitar exposición pública.
    """

    _require_internal_token(x_internal_token)

    await notify_websocket(
        room="payments",
        event=payload.event,
        message="Evento externo procesado por n8n",
        data={
            "paymentId": payload.paymentId,
            "partnerId": payload.partnerId,
            "amount": payload.amount,
            "currency": payload.currency,
            "extra": payload.extra or {},
        },
    )

    return {"status": "activated", "event": payload.event}


class EmailIn(BaseModel):
    to: str
    subject: str
    body: str


@router.post("/send-email")
def send_email(
    payload: EmailIn,
    x_internal_token: Optional[str] = Header(default=None, alias="X-Internal-Token"),
):
    """Envío de email (demostrable localmente).

    Por defecto se puede usar MailHog (SMTP) vía docker-compose.
    """

    _require_internal_token(x_internal_token)

    smtp_host = (os.getenv("SMTP_HOST") or "").strip()
    smtp_port = int((os.getenv("SMTP_PORT") or "1025").strip())
    smtp_from = (os.getenv("SMTP_FROM") or "noreply@local.test").strip()

    if not smtp_host:
        raise HTTPException(status_code=500, detail="SMTP_HOST no está configurado")

    message = EmailMessage()
    message["From"] = smtp_from
    message["To"] = payload.to
    message["Subject"] = payload.subject
    message.set_content(payload.body)

    try:
        with smtplib.SMTP(host=smtp_host, port=smtp_port, timeout=5) as smtp:
            smtp.send_message(message)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"No se pudo enviar email: {exc}")

    return {"status": "sent", "to": payload.to}
