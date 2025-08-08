from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from logger import get_logger
logger = get_logger(__name__)

class ReceiptNodeStrategy(GraphStrategyInterface):
    
    def build(self, state: GraphState) -> GraphState:
        """
        Gera um comprovante para a transação.
        """

        logger.info("Node: Receipt iniciado")

        state.receipt.receipt_id = "1234567890"
        state.trace.append("receipt")

        logger.info("Node: Receipt finalizado")

        return state
