from graph.graph_state import GraphState
from infra.openai_client import OpenAIClientFactory
from pipeline.openai import Key
from langchain_openai.chat_models import ChatOpenAI
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from datetime import datetime

import json

from logger import get_logger
logger = get_logger(__name__)

class VerifyLimitValueNodeStrategy(GraphStrategyInterface):
    
    def build(self, state: GraphState) -> GraphState:
        """
        Verifica se o cliente mencionou um valor monetário para atualizar o limite.
        """
        super().build(state) 

        logger.info("Node: Verify Limit Value")

        api_key = Key.get_openai_key()
        openai_client = OpenAIClientFactory(api_key=api_key)
        chat: ChatOpenAI = openai_client.create_basic_client()

        prompt = self.get_prompt(state)

        response = chat.invoke(prompt)
        result = json.loads(response.content)

        logger.info("================================================")
        logger.info(f"Resposta: {response.content}")
        logger.info("================================================")

        if result["tem_valor"] is True:
            state.limit.value = result["valor"]
            state.limit.last_update = datetime.now()
            state.limit.has_limit = True
        else: 
            state.limit.value = None
            state.limit.has_limit = False
            state.answer = result["resposta"]

        return state

    def get_prompt(self, state: GraphState) -> str:
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

        return prompt.strip()
