from graph.graph_state import GraphState
from infra.client_singleton import get_client_instance
from pipeline.openai import Key
from langchain_openai.chat_models import ChatOpenAI
from graph.nodes.graph_strategy_interface import GraphStrategyInterface
from model.pix import PixModel

from langchain_core.prompts import ChatPromptTemplate

from commons.logger import get_logger
logger = get_logger(__name__)

class CheckValueKeyNodeStrategy(GraphStrategyInterface):
    
    def name() -> str:
        return "check_value_key"
    
    def build(self, state: GraphState) -> GraphState:
        """
        Verifica se o cliente mencionou um valor ou chave Pix.
        """
        super().build(state) 
        logger.info("Node: Check Value Key")

        chat: ChatOpenAI = get_client_instance()

        structured_output = chat.with_structured_output(PixModel)
        chain = self.get_prompt() | structured_output

        response = chain.invoke({"mensagem": state.user_message})

        logger.info("================================================")
        logger.info(f"Resposta: {response}")
        logger.info("================================================")

        logger.info(f"response.tem_valor: {response.has_value}")
        logger.info(f"response.tem_chave: {response.has_key}")
        logger.info(f"response.valor: {response.value}")
        logger.info(f"response.chave: {response.key}")
        logger.info(f"response.more_information: {response.more_information}")

        if response.has_value:
            state.pix.value = response.value
            state.pix.has_value = True
        
        if response.has_key:
            state.pix.key = response.key
            state.pix.has_key = True
        
        if response.more_information:
            state.answer = response.more_information

        return state

    def get_prompt(self) -> str:
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "Você extrai dados de pagamentos Pix. Se não souber algum campo, deixe nulo."
                "Se faltar algo (chave e/ou valor), escreva em 'more_information' "
                "uma pergunta objetiva e curta pedindo o que falta. "
            ),
            (
                "human",
                "Texto do usuário: {mensagem} "
                "Identifique se há chave Pix (cpf/cnpj/email/telefone), o tipo, e valor em BRL."
            )
        ])

        return prompt