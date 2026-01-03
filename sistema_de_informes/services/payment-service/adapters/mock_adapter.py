from __future__ import annotations

import secrets
from typing import Any, Dict

from adapters.provider import PaymentProvider
from domain.models import PaymentRecord
from storage.in_memory import InMemoryPaymentStore


class MockAdapter(PaymentProvider):
    """Proveedor de pagos simulado.

    - Genera IDs únicos
    - Simula pagos exitosos y fallidos
    - Cambia estado del pago (pending -> succeeded/failed)
    """

    def __init__(self, store: InMemoryPaymentStore, provider_name: str = "mock") -> None:
        self._store = store
        self._provider_name = provider_name

    def create_payment(self, data: Dict[str, Any]) -> PaymentRecord:
        payment_id = f"pay_{secrets.token_hex(8)}"

        record = PaymentRecord(
            id=payment_id,
            provider=self._provider_name,
            status="pending",
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
        if event == "payment.success":
            return self._store.update_status(payment_id, "succeeded")
        if event == "payment.failed":
            return self._store.update_status(payment_id, "failed")
        if event == "payment.pending":
            return self._store.update_status(payment_id, "pending")
        return None
