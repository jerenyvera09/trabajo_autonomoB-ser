from __future__ import annotations

import json
import os
import secrets
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from adapters.mock_adapter import MockAdapter
from adapters.provider import PaymentProvider
from domain.models import Partner
from domain.schemas import (
    CheckoutIn,
    NormalizedWebhookEvent,
    PartnerRegisterIn,
    PartnerRegisterOut,
    PaymentOut,
)
from security.hmac_utils import verify_hmac_sha256
from security.hmac_utils import compute_hmac_sha256
from storage.in_memory import InMemoryPartnerStore, InMemoryPaymentStore
from webhooks.normalize import normalize_webhook

load_dotenv()

app = FastAPI(title="Payment Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Almacenamiento en memoria (Semana 2: NO DB)
payment_store = InMemoryPaymentStore()
partner_store = InMemoryPartnerStore()


def get_provider() -> PaymentProvider:
    provider = (os.getenv("PAYMENT_PROVIDER") or "mock").lower()
    if provider == "mock":
        return MockAdapter(payment_store, provider_name="mock")

    # No implementado en Semana 2
    raise HTTPException(status_code=400, detail=f"Provider no soportado en Semana 2: {provider}")


@app.get("/")
def root():
    return {"status": "ok", "service": "payment-service"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "payment-service"}


@app.post("/payments/checkout", response_model=PaymentOut, status_code=201)
def checkout(payload: CheckoutIn):
    provider = get_provider()
    record = provider.create_payment(payload.model_dump())
    return PaymentOut(
        id=record.id,
        provider=record.provider,
        status=record.status,
        amount=record.amount,
        currency=record.currency,
    )


@app.get("/payments/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: str):
    provider = get_provider()
    record = payment_store.get(payment_id)
    if not record:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    # Status desde el provider (para MockAdapter es el mismo store)
    status = provider.get_payment_status(payment_id)
    return PaymentOut(
        id=record.id,
        provider=record.provider,
        status=status,
        amount=record.amount,
        currency=record.currency,
    )


@app.get("/payments", response_model=list[PaymentOut])
def list_payments():
    provider = get_provider()
    records = payment_store.list_all()
    out: list[PaymentOut] = []
    for r in records:
        # resolver status desde provider (para mock es el mismo store)
        status = provider.get_payment_status(r.id)
        out.append(
            PaymentOut(
                id=r.id,
                provider=r.provider,
                status=status,
                amount=r.amount,
                currency=r.currency,
            )
        )
    return out


@app.post("/partners/register", response_model=PartnerRegisterOut, status_code=201)
def register_partner(payload: PartnerRegisterIn):
    partner_id = f"partner_{secrets.token_hex(8)}"
    secret_value = secrets.token_hex(32)  # secret compartido para HMAC

    partner = Partner(
        id=partner_id,
        name=payload.name,
        webhook_url=payload.webhookUrl,
        events=list(payload.events),
        secret=secret_value,
    )
    partner_store.put(partner)

    return PartnerRegisterOut(
        partnerId=partner.id,
        name=partner.name,
        webhookUrl=partner.webhook_url,
        events=partner.events,
        secret=partner.secret,
    )


@app.post("/webhooks/{provider}", response_model=NormalizedWebhookEvent)
async def receive_webhook(
    provider: str,
    request: Request,
    x_signature: Optional[str] = Header(default=None, alias=os.getenv("HMAC_HEADER_SIGNATURE") or "X-Signature"),
    x_partner_id: Optional[str] = Header(default=None, alias=os.getenv("HMAC_HEADER_PARTNER_ID") or "X-Partner-Id"),
):
    raw_body = await request.body()

    provider_lower = (provider or "").lower()

    # Semana 2 (requisito literal): HMAC-SHA256 en TODOS los webhooks.
    # - provider == "partner": secret por partner registrado
    # - provider == "mock" / "stripe" (y cualquier otro no-partner): secret fallback del servicio
    if not x_signature:
        raise HTTPException(status_code=401, detail="Falta firma HMAC")

    # Si el webhook viene de un partner, validamos HMAC (Semana 2)
    if provider_lower == "partner":
        if not x_partner_id:
            raise HTTPException(status_code=400, detail="Falta X-Partner-Id")
        partner = partner_store.get(x_partner_id)
        if not partner:
            raise HTTPException(status_code=404, detail="Partner no registrado")

        if not verify_hmac_sha256(partner.secret, raw_body, x_signature):
            raise HTTPException(status_code=401, detail="Firma HMAC inválida")
    else:
        fallback_secret = os.getenv("PAYMENT_SERVICE_SECRET_FALLBACK") or "dev-secret-change-me"
        if not verify_hmac_sha256(fallback_secret, raw_body, x_signature):
            raise HTTPException(status_code=401, detail="Firma HMAC inválida")

    # Parsear JSON (si es inválido, FastAPI no lo parsea: lo hacemos manual)
    try:
        payload: Dict[str, Any] = await request.json()
    except Exception:
        payload = {}

    normalized = normalize_webhook(provider=provider, payload=payload)

    # Aplicar efecto si corresponde al MockAdapter (cambio de estado)
    if normalized.get("provider") == "mock":
        adapter = MockAdapter(payment_store, provider_name="mock")
        payment_id = str(normalized.get("paymentId") or "")
        event = str(normalized.get("event") or "")
        if payment_id:
            adapter.apply_webhook_event(payment_id, event)

    return NormalizedWebhookEvent(**normalized)


def _http_post_json(url: str, body: bytes, headers: Dict[str, str], timeout_seconds: int = 10) -> Dict[str, Any]:
    req = urllib.request.Request(url=url, data=body, method="POST")
    for k, v in headers.items():
        req.add_header(k, v)

    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            resp_body = resp.read().decode("utf-8", errors="replace")
            return {"status_code": int(getattr(resp, "status", 0) or 0), "response_body": resp_body}
    except urllib.error.HTTPError as e:
        err_body = ""
        try:
            err_body = e.read().decode("utf-8", errors="replace")
        except Exception:
            err_body = ""
        return {"status_code": int(getattr(e, "code", 0) or 0), "response_body": err_body}
    except Exception as e:
        return {"status_code": 0, "response_body": f"request_failed: {e}"}


@app.post("/partners/{partner_id}/send-test")
def send_test_webhook_to_partner(partner_id: str):
    """
    Semana 3: demostrar dirección "nuestro sistema -> partner".
    Envía un webhook firmado (HMAC-SHA256) al webhook_url del partner registrado.

    - Firma en header: X-Signature
    - Identificación: X-Partner-Id
    """

    partner = partner_store.get(partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner no registrado")

    payload = {
        "event": "payment.success",
        "data": {"payment_id": f"pay_{secrets.token_hex(6)}", "amount": 10.0, "currency": "USD"},
        "timestamp": "2026-01-15T00:00:00Z",
        "source": "payment-service",
    }

    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    signature = compute_hmac_sha256(partner.secret, body)

    result = _http_post_json(
        url=partner.webhook_url,
        body=body,
        headers={
            "Content-Type": "application/json",
            "X-Signature": signature,
            "X-Partner-Id": partner.id,
        },
        timeout_seconds=10,
    )

    return {
        "status": "sent",
        "partnerId": partner.id,
        "webhookUrl": partner.webhook_url,
        "event": payload["event"],
        "downstream": result,
    }
