from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass(slots=True)
class PaymentRecord:
    id: str
    provider: str
    status: str
    amount: float
    currency: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Partner:
    id: str
    name: str
    webhook_url: str
    events: list[str]
    secret: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
