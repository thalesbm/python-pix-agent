from typing import Callable
import streamlit as st
from datetime import datetime

from graph.state.graph_state import GraphState

from commons.logger import get_logger
logger = get_logger(__name__)

class MainView:
    """Classe responsável pela interface de usuário usando Streamlit com modelo de chat."""

    @staticmethod
    def set_view(callback: Callable[[str, str], GraphState]) -> None:
        """
        Configura a view de chat.
        """
        logger.info("Configurando View de Chat")
        
        users = {
            "123123123": "João",
            "456456456": "Maria",
            "789789789": "Pedro"
        }

        selected_user = st.selectbox(
            "Selecione o Usuário:",
            options=list(users.keys()),
            format_func=lambda uid: users[uid]
        )
        selected_name = users[selected_user]

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
                    if "name" in message and message["name"]:
                        st.markdown(message["name"])
                    
                    st.markdown(message["content"])
                    
                    if "details" in message and message["details"]:
                        st.markdown(message["details"])
                    
        if prompt := st.chat_input("Digite sua mensagem aqui..."):
            st.session_state.messages.append({
                "role": "user", 
                "name": selected_name,
                "content": prompt,
                "timestamp": datetime.now()
            })
            
            with st.chat_message("user"):
                st.markdown(selected_name)
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Processando sua solicitação..."):
                    state = callback(prompt, selected_user)
                    
                    response_content = state.answer
                    response_details = state.trace
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_content,
                        "details": response_details,
                        "timestamp": datetime.now()
                    })
                    
                    st.markdown(response_content)
                    st.markdown(response_details)
