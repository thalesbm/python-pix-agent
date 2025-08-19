from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from commons.logger import get_logger
logger = get_logger(__name__)

class CleanStateNodeStrategy(GraphStrategyInterface):
    
    def name() -> str:
        return "clean_state"
    
    def build(self, state: GraphState) -> GraphState:
        """
        Limpa o estado do grafo.
        """
        super().build(state) 

        logger.info("Node: CleanState") 

        return state
