from __future__ import annotations

import re
from typing import Any, Dict

from tools.base import MCPTool
from tools.create_payment_tool import CreatePaymentTool
from tools.activate_service_tool import ActivateServiceTool


def _safe_text(args: Dict[str, Any]) -> str:
    text = args.get("text")
    if not isinstance(text, str) or not text.strip():
        return ""
    # Normalizar espacios para análisis simple
    return re.sub(r"\s+", " ", text).strip()


def _extract_amount_guess(text: str) -> float | None:
    # Heurística simple: primer número decimal o entero razonable (ej: 123.45 o 123,45)
    m = re.search(r"(\d+[\.,]\d{1,2}|\d{1,6})", text)
    if not m:
        return None
    raw = m.group(1).replace(",", ".")
    try:
        value = float(raw)
    except Exception:
        return None
    if value <= 0:
        return None
    return value


class PdfInspectTool(MCPTool):
    """Tool (query) que consume texto extraído de PDF y devuelve un análisis simple."""

    name = "pdf_inspect"
    kind = "query"

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        text = _safe_text(args)
        if not text:
            return {"ok": False, "error": "missing_text", "message": "Provide extracted PDF text in toolArgs.text"}

        amount_guess = _extract_amount_guess(text)
        return {
            "ok": True,
            "chars": len(text),
            "words": len(text.split(" ")),
            "amount_guess": amount_guess,
            "note": "Inspección de PDF realizada localmente en tool (multimodal).",
        }


class PdfToPartnerPaymentTool(MCPTool):
    """Tool (action) Semana 4: PDF → crea pago → dispara webhook al partner vía payment-service."""

    name = "pdf_to_partner_payment"
    kind = "action"

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        text = _safe_text(args)
        if not text:
            return {"ok": False, "error": "missing_text", "message": "Provide extracted PDF text in toolArgs.text"}

        partner_id = str(args.get("partner_id", args.get("partnerId", ""))).strip()
        amount_override = args.get("amount")

        guessed = _extract_amount_guess(text)
        amount = None
        if isinstance(amount_override, (int, float)) and float(amount_override) > 0:
            amount = float(amount_override)
        elif guessed is not None:
            amount = guessed
        else:
            amount = 10.0

        payment_tool = CreatePaymentTool()
        payment_result = payment_tool.run({"amount": amount, "currency": "USD", "metadata": {"source": "pdf"}})

        activation_result = None
        if partner_id:
            activation_tool = ActivateServiceTool()
            activation_result = activation_tool.run({"partner_id": partner_id, "servicio": "pdf_payment"})

        return {
            "ok": True,
            "amount_used": amount,
            "payment": payment_result,
            "partner_activation": activation_result,
            "note": "Acción Semana 4: usa tools reales (payment-service + webhook partner).",
        }
