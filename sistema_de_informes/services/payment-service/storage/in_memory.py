from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from threading import RLock
from typing import Dict, Optional

from domain.models import Partner, PaymentRecord


class InMemoryPaymentStore:
    def __init__(self) -> None:
        self._lock = RLock()
        self._payments: Dict[str, PaymentRecord] = {}

    def put(self, payment: PaymentRecord) -> PaymentRecord:
        with self._lock:
            self._payments[payment.id] = payment
            return payment

    def get(self, payment_id: str) -> Optional[PaymentRecord]:
        with self._lock:
            return self._payments.get(payment_id)

    def update_status(self, payment_id: str, status: str) -> Optional[PaymentRecord]:
        with self._lock:
            existing = self._payments.get(payment_id)
            if not existing:
                return None
            updated = replace(existing, status=status, updated_at=datetime.now(timezone.utc))
            self._payments[payment_id] = updated
            return updated


class InMemoryPartnerStore:
    def __init__(self) -> None:
        self._lock = RLock()
        self._partners: Dict[str, Partner] = {}

    def put(self, partner: Partner) -> Partner:
        with self._lock:
            self._partners[partner.id] = partner
            return partner

    def get(self, partner_id: str) -> Optional[Partner]:
        with self._lock:
            return self._partners.get(partner_id)
