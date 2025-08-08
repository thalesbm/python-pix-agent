from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from logger import get_logger
logger = get_logger(__name__)

class CleanStateNodeStrategy(GraphStrategyInterface):
    
    def build(self, state: GraphState) -> GraphState:
        """
        Limpa o estado do grafo.
        """

        logger.info("Node: CleanState")

        state.trace.append("clean_state")

        return state
