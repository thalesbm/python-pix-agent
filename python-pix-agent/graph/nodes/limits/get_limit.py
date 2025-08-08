from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from service.limit.limit_service import LimitService

from logger import get_logger
logger = get_logger(__name__)

class GetLimitNodeStrategy(GraphStrategyInterface):
    
    def build(self, state: GraphState) -> GraphState:
        """
        Obtém o limite do cliente.
        """
        super().build(state) 

        logger.info("Node: Get Limit")

        limit_service = LimitService()
        state.limit = limit_service.get()
        
        return state
