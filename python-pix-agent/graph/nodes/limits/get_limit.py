from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from datetime import datetime

from logger import get_logger
logger = get_logger(__name__)

class GetLimitNodeStrategy(GraphStrategyInterface):
    
    def build(self, state: GraphState) -> GraphState:
        """
        Obtém o limite do cliente.
        """

        logger.info("Node: Get Limit")

        state.limit.value = 1000
        state.limit.last_update = datetime.now()
        state.trace.append("get_limit")
        
        return state
