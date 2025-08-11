from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from logger import get_logger
logger = get_logger(__name__)

class FinishSimpleFlowNodeStrategy(GraphStrategyInterface):
    
    def name() -> str:
        return "finish_simple_flow"
    
    def build(self, state: GraphState) -> GraphState:
        """
        Finaliza o fluxo simples.
        """
        super().build(state) 

        logger.info("Node: Finish Simple Flow")

        return state
