from controller.main_controller import MainController
from config import get_config
from logger import setup_logging, get_logger
from view.main_view import MainView
import streamlit as st

from graph.graph_state import GraphState

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
    """
    Processa a mensagem recebida.
    """
    if "graph_state" not in st.session_state:
        st.session_state.graph_state = GraphState(user_message=message)

    logger.info(f"Mensagem recebida: {message}")
    state = MainController().run(message=message, state=st.session_state.graph_state)
    st.session_state.graph_state = state

    return state

if __name__ == "__main__":
    init()