from graph.graph_state import GraphState
from infra.openai_client import OpenAIClientFactory
from pipeline.openai import Key
from langchain_openai.chat_models import ChatOpenAI

import json

from logger import get_logger
logger = get_logger(__name__)

def check_value_key(state: GraphState) -> GraphState:
    logger.info("Node: Check Value Key")

    api_key = Key.get_openai_key()
    openai_client = OpenAIClientFactory(api_key=api_key)
    chat: ChatOpenAI = openai_client.create_basic_client()

    prompt = f"""
        Você é um assistente bancário. Seu objetivo é analisar a mensagem do cliente e identificar se ela contém:

        1. Uma **chave Pix**, que pode ser:
        - CPF (formato: 000.000.000-00 ou apenas números)
        - CNPJ (formato: 00.000.000/0000-00 ou apenas números)
        - E-mail
        - Telefone (com ou sem DDD, com ou sem +55)

        2. Um **valor monetário**, como "R$ 200", "300 reais", "mil", "1500", etc.
        Retorne **exclusivamente** um JSON com os seguintes campos:
        - `"tem_valor"`: `true` ou `false`, dependendo se um valor foi identificado
        - `"tem_chave"`: `true` ou `false`, dependendo se uma chave Pix foi identificada
        - `"valor"`: o valor numérico identificado
        - `"chave"`: a chave Pix identificada
        - `"resposta"`: uma mensagem amigável e breve para o cliente, **somente se faltar alguma informação**

        3. Considere também o histórico abaixo (informações já conhecidas de mensagens anteriores):
        - Se o cliente **não mencionou nenhuma nova informação**, mantenha os dados anteriores.
        - Se ele mencionou **apenas a chave Pix**, use a nova chave mas mantenha o valor anterior.
        - Se ele mencionou **apenas o valor**, atualize o valor mas mantenha a chave anterior.
        - Se ele **não mencionar nada novo**, apenas copie os valores já existentes para o JSON final.

        Histórico anterior:
        - Chave anterior: "{state.pix.key}"
        - Tinha chave: "{state.pix.has_key}"
        - Valor anterior: "{state.pix.value}"
        - Tinha valor: "{state.pix.has_value}"

        Retorne apenas o JSON, sem aspas, sem explicações, sem blocos de código:
        {{"tem_valor": true, "tem_chave": false, "valor": 200, "chave": "", "resposta": "Qual é a chave Pix para envio?"}}

        Mensagem do cliente: "{state.user_message}"
    """

    response = chat.invoke(prompt)
    result = json.loads(response.content)

    logger.info("================================================")
    logger.info(f"Resposta: {response.content}")
    logger.info("================================================")

    if result["tem_valor"]:
        state.pix.value = result["valor"]
        state.pix.has_value = True
    
    if result["tem_chave"]:
        state.pix.key = result["chave"]
        state.pix.has_key = True
    
    state.answer = result["resposta"]

    state.trace.append("check_value_key")

    return state
