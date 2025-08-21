"""
Infrastructure module - Responsável por configurações de infraestrutura e clientes externos.
"""

from .openai_client import OpenAIClientFactory
from .client_singleton import get_client_instance

__all__ = [
    "OpenAIClientFactory",
    "get_client_instance"
] 