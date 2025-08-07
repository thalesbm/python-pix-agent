from graph.graph_state import GraphState

from graph.graph_state import GraphState
from infra.openai_client import OpenAIClientFactory
from pipeline.openai import Key
from langchain_openai.chat_models import ChatOpenAI 

from logger import get_logger
logger = get_logger(__name__)

def format_answer_from_state(state: GraphState) -> GraphState:
    """
    Formata a mensagem para o formato de entrada do modelo.
    """

    logger.info("Iniciando processo de formatar resposta...")

    api_key = Key.get_openai_key()
    openai_client = OpenAIClientFactory(api_key=api_key)
    chat: ChatOpenAI = openai_client.create_basic_client()

    prompt = get_prompt(state)
    response = chat.invoke(prompt)

    logger.info("================================================")
    logger.info("Resposta final:", response.content)
    logger.info("================================================")

    state.answer = response.content
    state.trace.append("format_answer_from_state")

    return state

def get_prompt(state: GraphState) -> str:
    prompt = f"""
        Você é um assistente bancário objetivo. Gere uma resposta natural, clara e útil com base nas informações abaixo extraídas do estado atual do cliente.

        **Instruções:**
        - Responda **apenas** com as informações relevantes para a intenção informada.
        - Se a intenção for **consultar saldo**, responda apenas com o saldo com uma mensagem amigável.
        - Se a intenção for **consultar limite**, responda apenas com o limite com uma mensagem amigável.
        - Se a intenção for **atualizar limite**, responda apenas com o limite com uma mensagem amigável e o comprovante.
        - Formate valores como moeda brasileira (ex: R$ 100,00).
        - Se houver datas, formate como **dd/mm/aaaa**.
        - Se não houver dados disponíveis, informe que houve um erro e sugira tentar novamente.

        **Informações:**
        - Intenção: {state.intention}
        - Saldo: {state.balance.value if state.balance and state.balance.value else 'não disponível'}
        - Limite: {state.limit.value if state.limit and state.limit.value else 'não disponível'}
        - Comprovante: {state.receipt.receipt_id if state.receipt and state.receipt.receipt_id else 'não disponível'}
    """

    return prompt.strip()