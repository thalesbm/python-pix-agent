from model.graph_state import GraphState
from infra.openai_client import OpenAIClientFactory
from pipeline.openai import Key
from langchain_openai.chat_models import ChatOpenAI

from logger import get_logger
logger = get_logger(__name__)

def check_intention(state: GraphState) -> GraphState:
    logger.info(f"Recebendo o estado: {state}")

    api_key = Key.get_openai_key()
    openai_client = OpenAIClientFactory(api_key=api_key)
    chat: ChatOpenAI = openai_client.create_basic_client()

    prompt = f"""
        A partir da mensagem do cliente, identifique uma das seguintes intenções:
        - consultar_limite
        - agendar_pix
        - realizar_pix
        - cancelar_agendamento

        Mensagem: "{state.user_message}"
        Intenção:"""

    response = chat.invoke(prompt)

    state.intention = response.content

    logger.info("================================================")
    logger.info(f"Prompt: {prompt}")
    logger.info(f"Intenção: {state.intention}")
    logger.info(f"Resposta: {response.content}")
    logger.info("================================================")

    return state
