from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from tools.base import MCPTool
from typing import Any, Dict

class QueryPaymentTool(MCPTool):
    """
    Tool de consulta de pago (real en Semana 3).
    Consulta un pago llamando al payment-service.
    """
    name = "query_payment"
    kind = "query"

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        base_url = os.getenv("PAYMENT_SERVICE_URL") or "http://payment-service:8002"
        payment_id = str(args.get("payment_id", args.get("paymentId", args.get("id", ""))))
        if not payment_id:
            return {"ok": False, "error": "missing_payment_id", "message": "Provide payment_id"}

        try:
            url = f"{base_url}/payments/{payment_id}"
            req = urllib.request.Request(url, method="GET", headers={"Accept": "application/json"})
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
                "error": "payment_not_found_or_error",
                "status_code": int(getattr(e, "code", 500)),
                "response": error_body or str(e),
            }
        except Exception as e:
            return {"ok": False, "error": "payment_service_unreachable", "detail": str(e), "base_url": base_url}

        if status_code >= 400:
            return {"ok": False, "error": "payment_not_found_or_error", "status_code": status_code, "response": resp_body}

        try:
            data = json.loads(resp_body) if resp_body else {}
        except Exception:
            data = {"raw": resp_body}

        return {"ok": True, "payment": data}
