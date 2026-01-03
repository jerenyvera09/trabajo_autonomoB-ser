from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class ChatIn(BaseModel):
    message: str = Field(..., min_length=1)
    # Para demo local: permitir invocar tool directamente
    toolName: Optional[str] = Field(default=None, description="info | action")
    toolArgs: Dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    tool: str
    result: Dict[str, Any]


class ChatOut(BaseModel):
    provider: str
    reply: str
    toolsUsed: List[ToolResult] = Field(default_factory=list)
