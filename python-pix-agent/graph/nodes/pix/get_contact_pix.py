from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from commons.logger import get_logger
logger = get_logger(__name__)

class GetContactPixNodeStrategy(GraphStrategyInterface):
    
    def name() -> str:
        return "get_contact_pix"
    
    def build(self, state: GraphState) -> GraphState:
        """
        Obtém o contato do cliente.
        """
        super().build(state) 

        logger.info("Node: Get Contact Pix")

        return state
