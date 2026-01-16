from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from tools.base import MCPTool
from typing import Any, Dict

class ActivateServiceTool(MCPTool):
    """
    Tool de acción: activar servicio (mock).
    Simula la activación de un servicio.
    // STOP: Para integración real, conectar con el microservicio correspondiente.
    """
    name = "activate_service"
    kind = "action"

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        base_url = os.getenv("PAYMENT_SERVICE_URL") or "http://payment-service:8002"
        partner_id = str(args.get("partner_id", args.get("partnerId", ""))).strip()
        servicio = args.get("servicio", "demo")

        if not partner_id:
            return {
                "ok": False,
                "error": "missing_partner_id",
                "message": "Provide partner_id to send a signed event via payment-service (/partners/{id}/send-test).",
                "servicio": servicio,
            }

        try:
            url = f"{base_url}/partners/{partner_id}/send-test"
            req = urllib.request.Request(url, data=b"", method="POST", headers={"Accept": "application/json"})
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
                "base_url": base_url,
            }
        except Exception as e:
            return {"ok": False, "error": "payment_service_unreachable", "detail": str(e), "base_url": base_url}

        if status_code >= 400:
            return {"ok": False, "error": "payment_service_error", "status_code": status_code, "response": resp_body}

        try:
            data = json.loads(resp_body) if resp_body else {}
        except Exception:
            data = {"raw": resp_body}

        return {
            "ok": True,
            "servicio": servicio,
            "estado": "activado",
            "accion": "send_test_webhook",
            "partner_id": partner_id,
            "downstream": data,
            "note": "Acción real: dispara webhook firmado al partner vía payment-service.",
        }
