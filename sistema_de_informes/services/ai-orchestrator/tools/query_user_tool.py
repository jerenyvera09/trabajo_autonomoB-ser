from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from tools.base import MCPTool
from typing import Any, Dict

class QueryUserTool(MCPTool):
    """
    Tool de consulta de usuario (mock).
    Devuelve datos simulados.
    // STOP: Para integración real, conectar con auth-service.
    """
    name = "query_user"
    kind = "query"

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        # Semana 3 (sin tocar auth-service): si el caller provee un token,
        # validamos contra auth-service para devolver datos reales del claim.
        token = str(args.get("token") or args.get("access_token") or "").strip()
        auth_base_url = os.getenv("AUTH_SERVICE_URL") or "http://auth-service:8001"

        if token:
            try:
                qs = urllib.parse.urlencode({"token": token})
                url = f"{auth_base_url}/auth/validate?{qs}"
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
                    "error": "auth_service_error",
                    "status_code": int(getattr(e, "code", 500)),
                    "response": error_body or str(e),
                    "base_url": auth_base_url,
                }
            except Exception as e:
                return {"ok": False, "error": "auth_service_unreachable", "detail": str(e), "base_url": auth_base_url}

            if status_code >= 400:
                return {"ok": False, "error": "auth_service_error", "status_code": status_code, "response": resp_body}

            try:
                data = json.loads(resp_body) if resp_body else {}
            except Exception:
                data = {"raw": resp_body}

            return {"ok": True, "validation": data, "note": "Validación real vía auth-service (/auth/validate)."}

        # Fallback: sin token seguimos respondiendo algo útil para demo.
        user_id = args.get("user_id", 1)
        return {
            "ok": True,
            "id_usuario": user_id,
            "nombre": "Usuario Demo",
            "email": "demo@example.com",
            "estado": "ACTIVO",
            "note": "Sin token: respuesta demo. Para respuesta real, provee 'token' y se consultará auth-service.",
        }
