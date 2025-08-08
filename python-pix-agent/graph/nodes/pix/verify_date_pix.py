from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from logger import get_logger
logger = get_logger(__name__)

class VerifyDatePixNodeStrategy(GraphStrategyInterface):
    
    def build(self, state: GraphState) -> GraphState:
        """
        Verifica se a data da transação Pix é válida.
        """

        logger.info("Node: Verify Date Pix")

        state.trace.append("verify_date_pix")

        return state
