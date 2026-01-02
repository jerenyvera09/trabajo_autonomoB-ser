from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from domain.models import PaymentRecord


class PaymentProvider(ABC):
    """Interfaz del Adapter Pattern.

    En Semana 2 usamos un proveedor simulado (MockAdapter) para demostrar el flujo sin depender
    de servicios externos.
    """

    @abstractmethod
    def create_payment(self, data: Dict[str, Any]) -> PaymentRecord:
        raise NotImplementedError

    @abstractmethod
    def get_payment_status(self, payment_id: str) -> str:
        raise NotImplementedError
