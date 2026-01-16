from __future__ import annotations

from llm.provider import LLMProvider

class RealLLMAdapter(LLMProvider):
    """
    Adapter preparado para integración real con un LLM externo (OpenAI, Gemini, etc).
    // STOP: Requiere configuración de API real y credenciales.
    """
    def generate(self, prompt: str) -> str:
        # STOP: Aquí se debe implementar la llamada real a la API del proveedor LLM.
        return "// STOP: Requiere integración real con proveedor LLM."
