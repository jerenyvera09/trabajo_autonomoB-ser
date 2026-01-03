from __future__ import annotations

from typing import Any, Dict

from adapters.provider import PaymentProvider
from domain.models import PaymentRecord


class StripeAdapter(PaymentProvider):
    """Placeholder (NO USADO en Semana 2).

    Se deja únicamente como referencia de extensión del Adapter Pattern.
    """

    def create_payment(self, data: Dict[str, Any]) -> PaymentRecord:
        raise NotImplementedError("StripeAdapter no está implementado en Semana 2")

    def get_payment_status(self, payment_id: str) -> str:
        raise NotImplementedError("StripeAdapter no está implementado en Semana 2")
