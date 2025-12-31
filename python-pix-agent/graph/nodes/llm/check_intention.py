from graph.graph_state import GraphState
from infra.openai_client import OpenAIClientFactory
from langchain_openai.chat_models import ChatOpenAI
from graph.nodes.graph_strategy_interface import GraphStrategyInterface
from google import genai
from google.genai import types

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

        client = genai.Client(api_key="AIzaSyCK790qqhAxdL1OD9lrpN1w05r6Rexjphk")

        prompt = self.get_prompt(state)

        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
        )
        state.intention = response.text

        # chat: ChatOpenAI = OpenAIClientFactory().create_basic_client()

        # response = chat.invoke(prompt)

        logger.info("================================================")
        logger.info(f"Prompt: {prompt}")
        logger.info(f"Intenção: {state.intention}")
        logger.info(f"Resposta: {response.text}")
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
