from __future__ import annotations

from typing import Any, Dict

from tools.base import MCPTool


class ActionTool(MCPTool):
    name = "action"
    kind = "action"

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        action = str(args.get("action") or "simulate")
        target = str(args.get("target") or "local")
        return {
            "ok": True,
            "performed": action,
            "target": target,
            "note": "Acción simulada (Semana 2).",
        }
