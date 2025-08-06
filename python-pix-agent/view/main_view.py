from typing import Callable
import streamlit as st

from graph.graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

class MainView:
    """Classe responsável pela interface de usuário usando Streamlit."""

    @staticmethod
    def set_view(callback: Callable[[str], None]) -> None:
        logger.info("Configurando View")
        
        with st.container():
            with st.form(key="meu_formulario"):
                # Campo de pergunta
                question_input: str = st.text_area(
                    "Digite sua Intenção:",
                    value="quero fazer um pix",
                    height=60,
                )
                
                # Botão de envio
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    submit: bool = st.form_submit_button(
                        "Enviar Intenção",
                        use_container_width=True
                    )

        if submit:
            if question_input and question_input.strip():
                callback(question_input)
            else:
                st.error("❌ Por favor, insira uma pergunta antes de enviar.")

    @staticmethod
    def update_view_with_state(state: GraphState) -> None:
        st.subheader("Graph State:")
        st.write(state.answer)
        
       
