from graph.graph_state import GraphState
from infra.openai_client import OpenAIClientFactory
from langchain_openai.chat_models import ChatOpenAI
from graph.nodes.graph_strategy_interface import GraphStrategyInterface
from langgraph.types import interrupt

from datetime import datetime

import json

from commons.logger import get_logger
logger = get_logger(__name__)

class VerifyLimitValueNodeStrategy(GraphStrategyInterface):
    
    @staticmethod
    def name() -> str:
        return "verify_limit_value"
    
    def build(self, state: GraphState) -> GraphState:
        """
        Verifica se o cliente mencionou um valor monetário para atualizar o limite.
        Se não houver valor, interrompe o fluxo para solicitar a informação.
        """
        super().build(state) 

        logger.info("Node: Verify Limit Value")

        chat: ChatOpenAI = OpenAIClientFactory().create_basic_client()

        prompt = self.get_prompt(state)

        response = chat.invoke(prompt)

        logger.info("================================================")
        logger.info(f"Resposta: {response.content}")
        logger.info("================================================")

        state.trace.append("verify_limit_value")

        try:
            result = json.loads(response.content)
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao fazer parse do JSON: {e}")
            logger.error(f"Conteúdo da resposta: {response.content}")
            
            # Fallback: assume que não há valor e solicita informação
            state.limit.value = None
            state.limit.has_limit = False
            state.answer = "Desculpe, não consegui entender o valor. Pode me informar qual valor você deseja definir como novo limite?"
            
            raise interrupt(
                {
                     "message": state.answer,
                }
            )

        if result["tem_valor"] is True:
            state.limit.value = result["valor"]
            state.limit.last_update = datetime.now()
            state.limit.has_limit = True
        else: 
            state.limit.value = None
            state.limit.has_limit = False
            state.answer = result["resposta"]
            
            logger.info("Valor do limite não fornecido - interrompendo fluxo para solicitar informação")
            
            # Interrompe o fluxo e solicita o valor do limite
            raise interrupt(
                {
                    "message": result["resposta"],
                }
            )

        return state

    def get_prompt(self, state: GraphState) -> str:
        prompt = f"""
            Você é um assistente de atendimento bancário especializado em atualização de limites.
            
            Analise a mensagem do cliente e identifique se há um valor monetário para atualizar o limite.
            
            **Valores aceitos:**
            - Números: "500", "1000", "2000"
            - Com símbolo: "R$ 500", "R$ 1.000", "R$ 2.000"
            - Por extenso: "mil reais", "dois mil", "quinhentos reais"
            - Decimais: "500,50", "R$ 1.250,75"
            
            **Retorne EXATAMENTE um dos formatos JSON abaixo:**
            
            1. Se encontrar um valor monetário válido:
            {{"tem_valor": true, "valor": 2000}}
            
            2. Se NÃO encontrar valor ou valor for inválido:
            {{"tem_valor": false, "resposta": "Para atualizar seu limite, preciso saber qual valor você deseja definir. Pode me informar o valor desejado?"}}
            
            **Regras importantes:**
            - Extraia apenas o valor numérico (sem símbolos)
            - Se houver múltiplos valores, use o primeiro mencionado
            - Valores devem ser positivos e razoáveis (entre R$ 100 e R$ 50.000)
            - Se o valor for muito baixo ou muito alto, considere como inválido
            
            Mensagem do cliente: "{state.user_message}"
        """

        return prompt.strip()
