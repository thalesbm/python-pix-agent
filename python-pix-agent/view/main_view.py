from typing import Callable
import streamlit as st
from datetime import datetime

from graph.graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

class MainView:
    """Classe responsável pela interface de usuário usando Streamlit com modelo de chat."""

    @staticmethod
    def set_view(callback: Callable[[str], GraphState]) -> None:
        logger.info("Configurando View de Chat")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        st.set_page_config(
            page_title="PIX Agent - Chat",
            page_icon="💬",
            layout="wide"
        )

        with st.container():
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    
                    if "details" in message and message["details"]:
                        st.markdown(message["details"])
                    
        if prompt := st.chat_input("Digite sua mensagem aqui..."):
            st.session_state.messages.append({
                "role": "user", 
                "content": prompt,
                "timestamp": datetime.now()
            })
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Processando sua solicitação..."):
                    state = callback(prompt)
                    
                    response_content = state.answer
                    response_details = state.trace
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_content,
                        "details": response_details,
                        "timestamp": datetime.now()
                    })
                    
                    st.markdown(response_content)
                    st.markdown("Graph:")
                    st.markdown(response_details)
