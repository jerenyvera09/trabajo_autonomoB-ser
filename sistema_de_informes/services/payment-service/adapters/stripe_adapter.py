from __future__ import annotations

import secrets
from typing import Any, Dict

from adapters.provider import PaymentProvider
from domain.models import PaymentRecord
from storage.in_memory import InMemoryPaymentStore


class StripeAdapter(PaymentProvider):
    """Adapter Stripe (implementación local para demo).

    Para la evaluación del patrón Adapter, este adapter:
    - Crea pagos en el mismo store en memoria
    - Usa IDs con prefijo 'pi_' (payment intent)
    - Permite simular éxito/fallo igual que MockAdapter

    Nota: No usa SDK externo para mantener la demo 100% local.
    """

    def __init__(self, store: InMemoryPaymentStore) -> None:
        self._store = store

    def create_payment(self, data: Dict[str, Any]) -> PaymentRecord:
        payment_id = f"pi_{secrets.token_hex(8)}"

        record = PaymentRecord(
            id=payment_id,
            provider="stripe",
            status="requires_payment_method",
            amount=float(data.get("amount")),
            currency=str(data.get("currency", "USD")).upper(),
            metadata=dict(data.get("metadata") or {}),
        )
        self._store.put(record)

        simulate = (data.get("simulate") or "success").lower()
        final_status = "succeeded" if simulate != "fail" else "failed"
        self._store.update_status(payment_id, final_status)

        updated = self._store.get(payment_id)
        assert updated is not None
        return updated

    def get_payment_status(self, payment_id: str) -> str:
        existing = self._store.get(payment_id)
        return existing.status if existing else "not_found"

    def apply_webhook_event(self, payment_id: str, event: str) -> PaymentRecord | None:
        # Aceptamos eventos normalizados y eventos típicos de Stripe
        if event in ("payment.success", "payment_intent.succeeded", "checkout.session.completed"):
            return self._store.update_status(payment_id, "succeeded")
        if event in ("payment.failed", "payment_intent.payment_failed"):
            return self._store.update_status(payment_id, "failed")
        if event in ("payment.pending", "payment_intent.processing"):
            return self._store.update_status(payment_id, "pending")
        return None
