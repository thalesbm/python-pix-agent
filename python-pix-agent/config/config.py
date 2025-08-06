"""
Configuração centralizada do Python Pix Agent.
Configurações otimizadas para desenvolvimento.
"""

from .logging_config import LoggingConfig
from .openai_config import OpenAIConfig
from .streamlit_config import StreamlitConfig
from .graph_config import GraphConfig

class Config:
    """Classe principal de configuração para desenvolvimento."""
    
    def __init__(self):
        self.openai = OpenAIConfig()
        self.logging = LoggingConfig()
        self.streamlit = StreamlitConfig()
        self.graph = GraphConfig()

# Instância global de configuração
config = Config()

def get_config() -> Config:
    """Retorna a instância global de configuração."""
    return config 