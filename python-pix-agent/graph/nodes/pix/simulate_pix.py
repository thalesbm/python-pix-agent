from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from commons.logger import get_logger
logger = get_logger(__name__)

class SimulatePixNodeStrategy(GraphStrategyInterface):
    
    def name() -> str:
        return "simulate_pix"
    
    def build(self, state: GraphState) -> GraphState:
        """
        Simula a transação Pix.
        """
        super().build(state) 

        logger.info("Node: Simulate Pix")

        return state
