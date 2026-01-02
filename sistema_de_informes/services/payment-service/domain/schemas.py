from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class CheckoutIn(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Control explícito del MockAdapter (para demo local)
    simulate: Optional[str] = Field(default=None, description="success | fail")


class PaymentOut(BaseModel):
    id: str
    provider: str
    status: str
    amount: float
    currency: str


class WebhookIn(BaseModel):
    payload: Dict[str, Any] = Field(default_factory=dict)


class NormalizedWebhookEvent(BaseModel):
    event: str
    paymentId: str
    provider: str
    timestamp: str


class PartnerRegisterIn(BaseModel):
    name: str = Field(..., min_length=2)
    webhookUrl: str = Field(..., min_length=8)
    events: List[str] = Field(default_factory=list)


class PartnerRegisterOut(BaseModel):
    partnerId: str
    name: str
    webhookUrl: str
    events: List[str]
    secret: str
