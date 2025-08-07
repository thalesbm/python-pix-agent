from controller.main_controller import MainController
from config import get_config
from logger import setup_logging, get_logger
from view.main_view import MainView
import streamlit as st

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

    MainView.set_view(process_message)

def process_message(message: str):
    logger.info(f"Mensagem recebida: {message}")
    return MainController().run(message)

if __name__ == "__main__":
    init()