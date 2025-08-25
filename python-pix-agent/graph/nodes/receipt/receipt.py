from graph.state.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from commons.logger import get_logger
logger = get_logger(__name__)

class ReceiptNodeStrategy(GraphStrategyInterface):
    
    def name() -> str:
        return "receipt"
    
    def build(self, state: GraphState) -> GraphState:
        """
        Gera um comprovante para a transação.
        """
        super().build(state) 

        logger.info("Node: Receipt iniciado")

        state.receipt.receipt_id = "1234567890"

        return state
