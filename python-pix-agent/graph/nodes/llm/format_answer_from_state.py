from graph.graph_state import GraphState

from graph.graph_state import GraphState
from infra.openai_client import OpenAIClientFactory
from langchain_openai.chat_models import ChatOpenAI 
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from commons.logger import get_logger
logger = get_logger(__name__)

class FormatAnswerFromStateNodeStrategy(GraphStrategyInterface):
    
    def name() -> str:
        return "format_answer_from_state"
    
    def build(self, state: GraphState) -> GraphState:
        """
        Formata a mensagem para o formato de entrada do modelo.
        """
        super().build(state) 

        logger.info("Node: Format Answer From State")

        chat: ChatOpenAI = OpenAIClientFactory().create_basic_client()

        prompt = self.get_prompt(state)
        response = chat.invoke(prompt)

        logger.info("================================================")
        logger.info(f"Resposta final: {response.content}")
        logger.info("================================================")

        state.answer = response.content

        return state

    def get_prompt(self, state: GraphState) -> str:
        prompt = f"""
            Você é um assistente bancário objetivo. Gere uma resposta natural, clara e útil com base nas informações abaixo extraídas do estado atual do cliente.

            **Instruções:**
            - Responda **apenas** com as informações relevantes para a intenção informada.
            - Se a intenção for **consultar saldo**, responda apenas com o saldo com uma mensagem amigável.
            - Se a intenção for **consultar limite**, responda apenas com o limite com uma mensagem amigável.
            - Se a intenção for **atualizar limite**, responda apenas com o limite com uma mensagem amigável e o comprovante.
            - Se a intenção for **realizar pix**, responda apenas com o valor e a chave pix com uma mensagem amigável de efetivação e o comprovante.
            - Formate valores como moeda brasileira (ex: R$ 100,00).
            - Se houver datas, formate como **dd/mm/aaaa**.
            - Se não houver dados disponíveis, informe que houve um erro e sugira tentar novamente.

            **Informações:**
            - Intenção: {state.intention}
            - Saldo: {state.balance.value if state.balance and state.balance.value else 'não disponível'}
            - Limite: {state.limit.value if state.limit and state.limit.value else 'não disponível'}
            - Comprovante: {state.receipt.receipt_id if state.receipt and state.receipt.receipt_id else 'não disponível'}
            - Chave Pix: {state.pix.key if state.pix and state.pix.key else 'não disponível'}
            - Valor: {state.pix.value if state.pix and state.pix.value else 'não disponível'}
        """

        return prompt.strip()