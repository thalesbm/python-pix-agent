from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from logger import get_logger
logger = get_logger(__name__)

class GetContactPixNodeStrategy(GraphStrategyInterface):
    
    def build(self, state: GraphState) -> GraphState:
        """
        Obtém o contato do cliente.
        """

        logger.info("Node: Get Contact Pix")

        state.trace.append("get_contact_pix")

        return state
