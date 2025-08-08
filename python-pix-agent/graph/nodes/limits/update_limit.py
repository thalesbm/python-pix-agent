from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from logger import get_logger
logger = get_logger(__name__)

class UpdateLimitNodeStrategy(GraphStrategyInterface):
   
    def build(self, state: GraphState) -> GraphState:
        """
        Atualiza o limite do cliente.
        """

        logger.info("Node: Update Limit")

        state.trace.append("update_limit")
        
        return state
