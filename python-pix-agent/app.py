from controller.main_controller import MainController
from config import get_config
from view.main_view import MainView
import streamlit as st

from graph.graph_state import GraphState

from commons.logger import setup_logging, get_logger
logger = get_logger(__name__)

def init():
    config = get_config()

    setup_logging(
        level=config.logging.level,
        format_string=config.logging.format,
    )
    
    logger.info("Bem vindo ao melhor mini agente do mundo")

    MainView.set_view(process_message)

def process_message(message: str, user_id: str):
    """
    Processa a mensagem recebida.
    """
    logger.info(f"Mensagem recebida: {message}")
    state = MainController().run(message=message, user_id=user_id)

    return state

if __name__ == "__main__":
    init()