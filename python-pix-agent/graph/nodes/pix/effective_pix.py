from graph.state.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from commons.logger import get_logger
logger = get_logger(__name__)

class EffectivePixNodeStrategy(GraphStrategyInterface):
    
    def name() -> str:
        return "effective_pix"
    
    def build(self, state: GraphState) -> GraphState:
        """
        Efetiva a transação Pix.
        """
        super().build(state) 

        logger.info("Node: Effective Pix")

        return state
