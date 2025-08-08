from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from logger import get_logger
logger = get_logger(__name__)

class FinishSimpleFlowNodeStrategy(GraphStrategyInterface):
    
    def build(self, state: GraphState) -> GraphState:
        """
        Finaliza o fluxo simples.
        """

        logger.info("Node: Finish Simple Flow")

        state.trace.append("finish_simple_flow")

        return state
