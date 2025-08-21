from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface
from infra.client_singleton import get_client_instance
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

from commons.logger import get_logger
logger = get_logger(__name__)

class FallbackNodeStrategy(GraphStrategyInterface):
    
    def name() -> str:
        return "fallback"
    
    def build(self, state: GraphState) -> GraphState:
        """
        Fallback do grafo.
        """
        super().build(state) 

        logger.info("Node: Fallback")

        chat: ChatOpenAI = get_client_instance()

        prompt = self.get_prompt()

        response = chat.invoke(prompt)

        state.intention = "fallback"
        state.answer = response.content

        logger.info("================================================")
        logger.info(f"Prompt: {prompt}")
        logger.info(f"Intenção: {state.intention}")
        logger.info(f"Resposta: {response.content}")
        logger.info("================================================")

        return state

    def get_prompt(self) -> str:
        prompt = f"""
            Você é um assistente financeiro que não conseguiu identificar a intenção do usuário.
            - consultar_limite
            - alterar_limite
            - realizar_pix
            - consultar_saldo

            Retorne uma mensagem de erro amigavel para o cliente.
        """

        return prompt.strip()
