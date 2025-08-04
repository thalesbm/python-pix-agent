"""
Pipeline module - Contém os componentes do pipeline RAG (Loader, Splitter, Embedding, Retrieval, OpenAI, Evaluate).
"""

from .openai import Key

__all__ = [
    "Key",
] 