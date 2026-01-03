from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from tools.base import MCPTool


class InfoTool(MCPTool):
    name = "info"
    kind = "query"

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "service": "ai-orchestrator",
            "now": datetime.now(timezone.utc).isoformat(),
            "note": "Tool de consulta simple (Semana 2).",
        }
