from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from logger import get_logger
logger = get_logger(__name__)

class FallbackNodeStrategy(GraphStrategyInterface):
    
    def name() -> str:
        return "fallback"
    
    def build(self, state: GraphState) -> GraphState:
        """
        Fallback do grafo.
        """
        super().build(state) 

        logger.info("Node: Fallback")

        return state
