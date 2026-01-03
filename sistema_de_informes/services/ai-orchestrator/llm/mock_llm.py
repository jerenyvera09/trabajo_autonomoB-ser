from __future__ import annotations

from llm.provider import LLMProvider


class MockLLM(LLMProvider):
    """LLM simulado para Semana 2.

    Devuelve respuestas fijas y deterministas para demo local.
    """

    def generate(self, prompt: str) -> str:
        prompt = (prompt or "").strip()
        if not prompt:
            return "(mock) Recibí un mensaje vacío."
        return f"(mock) Respuesta fija. Mensaje recibido: {prompt}"
