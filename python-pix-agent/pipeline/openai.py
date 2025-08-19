import os
from commons.logger.logger_config import get_logger
from dotenv import load_dotenv

logger = get_logger(__name__)

load_dotenv()

class Key:
    """Classe responsável por gerenciar a chave da API OpenAI."""

    @staticmethod
    def get_openai_key() -> str:
        """
        Obtém a chave da API OpenAI.
        """
        api_key = os.getenv("OPENAI_API_KEY")

        if api_key:
            logger.info("OpenAI API key carregada com sucesso.")
        else:
            logger.warning("OpenAI API key não foi encontrada!")

        return api_key
