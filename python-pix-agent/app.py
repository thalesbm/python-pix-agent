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
    
    # Configura Streamlit
    st.set_page_config(
        page_title=config.streamlit.page_title,
        page_icon=config.streamlit.page_icon,
        layout=config.streamlit.layout,
        initial_sidebar_state=config.streamlit.initial_sidebar_state
    )
    
    logger.info("Bem vindo ao melhor mini agente do mundo")

    MainView.set_view(get_form)

def get_form(message: str):
    logger.info(f"Mensagem recebida: {message}")
    state = MainController().run(message)
    MainView.update_view_with_state(state)


if __name__ == "__main__":
    init()