from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from logger import get_logger
logger = get_logger(__name__)

class UpdateLimitNodeStrategy(GraphStrategyInterface):
   
    def name(self) -> str:
        return "update_limit"
    
    def build(self, state: GraphState) -> GraphState:
        """
        Atualiza o limite do cliente.
        """
        super().build(state) 

        logger.info("Node: Update Limit")
        
        return state
