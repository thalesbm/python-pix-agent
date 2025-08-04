"""
Configuração centralizada do Python Pix Agent.
Configurações otimizadas para desenvolvimento.
"""

from config.logging_config import LoggingConfig
from config.openai_config import OpenAIConfig

class Config:
    """Classe principal de configuração para desenvolvimento."""
    
    def __init__(self):
        self.openai = OpenAIConfig()
        self.logging = LoggingConfig()

# Instância global de configuração
config = Config()

def get_config() -> Config:
    """Retorna a instância global de configuração."""
    return config 