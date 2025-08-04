from dataclasses import dataclass

@dataclass
class OpenAIConfig:
    """Configurações da OpenAI."""
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_tokens: int = 1000