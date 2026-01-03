from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Interfaz (Strategy Pattern) para proveedores de LLM.

    Semana 2: solo se usa MockLLM, sin IA real ni APIs externas.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError
