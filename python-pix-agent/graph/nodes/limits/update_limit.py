from graph.graph_state import GraphState
from infra.openai_client import OpenAIClientFactory
from pipeline.openai import Key
from langchain_openai.chat_models import ChatOpenAI

from datetime import datetime

from logger import get_logger
logger = get_logger(__name__)

def update_limit(state: GraphState) -> GraphState:
    logger.info("Node: Update Limit")

    api_key = Key.get_openai_key()
    openai_client = OpenAIClientFactory(api_key=api_key)
    chat: ChatOpenAI = openai_client.create_basic_client()

    prompt = f"""
        Você é um assistente de atendimento bancário.
        
        1. Se houver um valor monetário mencionado (por exemplo: "500", "R$ 2.000", "mil reais", "dois mil"), extraia apenas o valor em formato numérico, sem símbolos ou texto.
            Retorne no formato JSON:
            {{"tem_valor": true, "valor": 2000}}

        2. Se não houver valor explícito, retorne uma resposta natural e breve pedindo ao cliente que informe o valor desejado para atualizar o limite.  
            Retorne no formato JSON:
            {{"tem_valor": false, "resposta": "Claro! Qual valor você quer definir como novo limite?"}}

        Mensagem do cliente: "{state.user_message}"
    """

    response = chat.invoke(prompt)

    if response.content["tem_valor"]:
        state.limit.value = response.content["valor"]
        state.limit.last_update = datetime.now()
    else: 
        None

    state.trace.append("update_limit")

    logger.info("================================================")
    logger.info(f"Prompt: {prompt}")
    logger.info(f"Resposta: {response.content}")
    logger.info("================================================")
    
    return state
