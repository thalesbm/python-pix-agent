"""
Infrastructure module - Responsável por configurações de infraestrutura e clientes externos.
"""

from .openai_client import OpenAIClientFactory

__all__ = [
    "OpenAIClientFactory"
] 