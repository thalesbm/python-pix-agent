from controller.main_controller import MainController
from config import get_config

from graph.graph_state import GraphState

from commons.logger import setup_logging, get_logger
logger = get_logger(__name__)

def init():
    # Carrega configuração
    config = get_config()
    
    # Configura logging centralizado
    setup_logging(
        level=config.logging.level,
        format_string=config.logging.format,
    )
    
    logger.info("Bem vindo ao melhor mini agente do mundo")

    process_message("saldo")

def process_message(message: str):
    """
    Processa a mensagem recebida.
    """

    logger.info(f"Mensagem recebida: {message}")
    state = MainController().run(message=message)
    print("Resposta do agente:", state.answer)

    return state

if __name__ == "__main__":
    init()