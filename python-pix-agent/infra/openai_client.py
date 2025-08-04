from langchain_openai.chat_models import ChatOpenAI
from config.config import get_config

class OpenAIClientFactory:
    """Factory para criar clientes OpenAI com diferentes configurações."""
    
    def __init__(self, api_key: str, model: str = None):
        self.api_key = api_key
        self.config = get_config()
        self.model = model or self.config.openai.model

    def create_basic_client(self) -> ChatOpenAI:
        return ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            temperature=self.config.openai.temperature,
            max_tokens=self.config.openai.max_tokens
        )

    def create_client_with_tools(self, tools) -> ChatOpenAI:
        return ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            temperature=self.config.openai.temperature,
            max_tokens=self.config.openai.max_tokens
        ).bind(functions=tools)