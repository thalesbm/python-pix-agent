from graph.graph_state import GraphState
from infra.openai_client import OpenAIClientFactory
from langchain_openai.chat_models import ChatOpenAI
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from commons.logger import get_logger
logger = get_logger(__name__)

class CheckIntentionNodeStrategy(GraphStrategyInterface):
    
    def name() -> str:
        return "check_intention"

    def build(self, state: GraphState) -> GraphState:
        """
        Verifica a intenção do cliente.
        """
        super().build(state) 

        logger.info(f"Recebendo o estado: {state}")

        chat: ChatOpenAI = OpenAIClientFactory().create_basic_client()

        prompt = self.get_prompt(state)

        response = chat.invoke(prompt)

        state.intention = response.content

        logger.info("================================================")
        logger.info(f"Prompt: {prompt}")
        logger.info(f"Intenção: {state.intention}")
        logger.info(f"Resposta: {response.content}")
        logger.info("================================================")

        return state

    def get_prompt(self, state: GraphState) -> str:
        prompt = f"""
            A partir da mensagem do cliente, identifique uma das seguintes intenções:
            - consultar_limite
            - alterar_limite
            - realizar_pix
            - consultar_saldo

            Retornar apenas a intenção, sem nenhum outro texto.

            Mensagem do usuário: "{state.user_message}"
        """

        return prompt.strip()
