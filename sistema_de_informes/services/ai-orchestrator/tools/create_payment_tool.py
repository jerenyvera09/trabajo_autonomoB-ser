from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from tools.base import MCPTool
from typing import Any, Dict

class CreatePaymentTool(MCPTool):
    """
    Tool de acción: crear pago (real en Semana 3).
    Crea un pago llamando al payment-service.
    """
    name = "create_payment"
    kind = "action"

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        base_url = os.getenv("PAYMENT_SERVICE_URL") or "http://payment-service:8002"

        # Soportar nombres en español o en inglés
        amount = args.get("amount", args.get("monto", 10.0))
        currency = args.get("currency", args.get("moneda", "USD"))
        metadata = args.get("metadata", {})
        simulate = args.get("simulate")

        payload: Dict[str, Any] = {
            "amount": float(amount),
            "currency": str(currency).upper(),
            "metadata": metadata if isinstance(metadata, dict) else {},
        }
        if simulate in ("success", "fail"):
            payload["simulate"] = simulate

        try:
            url = f"{base_url}/payments/checkout"
            body = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=body,
                method="POST",
                headers={"Content-Type": "application/json", "Accept": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                resp_body = resp.read().decode("utf-8")
                status_code = int(getattr(resp, "status", 200))
        except urllib.error.HTTPError as e:
            try:
                error_body = e.read().decode("utf-8")
            except Exception:
                error_body = ""
            return {
                "ok": False,
                "error": "payment_service_error",
                "status_code": int(getattr(e, "code", 500)),
                "response": error_body or str(e),
            }
        except Exception as e:
            return {"ok": False, "error": "payment_service_unreachable", "detail": str(e), "base_url": base_url}

        if status_code >= 400:
            return {"ok": False, "error": "payment_service_error", "status_code": status_code, "response": resp_body}

        try:
            data = json.loads(resp_body) if resp_body else {}
        except Exception:
            data = {"raw": resp_body}

        return {"ok": True, "payment": data, "note": "Creado vía payment-service"}
