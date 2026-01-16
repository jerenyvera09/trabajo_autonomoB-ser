from __future__ import annotations

from tools.base import MCPTool
from datetime import datetime, timezone
import json
from typing import Any, Dict

import os
import urllib.error
import urllib.request

class ReportTool(MCPTool):
    """
    Tool de reporte (real en Semana 3).
    Genera un resumen consultando el payment-service.
    """
    name = "report"
    kind = "report"

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        base_url = os.getenv("PAYMENT_SERVICE_URL") or "http://payment-service:8002"
        currency = str(args.get("currency", "USD")).upper()

        try:
            url = f"{base_url}/payments"
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
                "error": "payment_service_error",
                "status_code": int(getattr(e, "code", 500)),
                "response": error_body or str(e),
            }
        except Exception as e:
            return {"ok": False, "error": "payment_service_unreachable", "detail": str(e), "base_url": base_url}

        if status_code >= 400:
            return {"ok": False, "error": "payment_service_error", "status_code": status_code, "response": resp_body}

        try:
            payments = json.loads(resp_body) if resp_body else []
        except Exception:
            return {"ok": False, "error": "invalid_json_from_payment_service", "response": resp_body}

        if not isinstance(payments, list):
            return {"ok": False, "error": "unexpected_payload", "payments": payments}

        total_count = 0
        total_amount = 0.0
        by_status: Dict[str, int] = {}

        detail = []
        for p in payments:
            if not isinstance(p, dict):
                continue
            total_count += 1
            amount = float(p.get("amount") or 0.0)
            total_amount += amount
            status = str(p.get("status") or "unknown")
            by_status[status] = by_status.get(status, 0) + 1
            detail.append({
                "id": p.get("id"),
                "status": status,
                "amount": amount,
                "currency": p.get("currency"),
            })

        return {
            "ok": True,
            "total_pagos": total_count,
            "monto_total": round(total_amount, 2),
            "moneda": currency,
            "por_estado": by_status,
            "hasta": datetime.now(timezone.utc).date().isoformat(),
            "detalle": detail,
            "note": "Reporte generado consultando payment-service (/payments).",
        }
