from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class MCPTool(ABC):
    """Tool mínima estilo MCP.

    Semana 2: solo 2 tools simples e invocables.
    """

    name: str
    kind: str  # query | action

    @abstractmethod
    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
