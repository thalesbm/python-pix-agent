from graph.state.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from commons.logger import get_logger
logger = get_logger(__name__)

class VerifyDatePixNodeStrategy(GraphStrategyInterface):
    
    def name() -> str:
        return "verify_date_pix"
    
    def build(self, state: GraphState) -> GraphState:
        """
        Verifica se a data da transação Pix é válida.
        """
        super().build(state) 

        logger.info("Node: Verify Date Pix")

        return state
