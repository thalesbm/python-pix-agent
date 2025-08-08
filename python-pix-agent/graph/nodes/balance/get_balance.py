from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from logger import get_logger
logger = get_logger(__name__)

class GetBalanceNodeStrategy(GraphStrategyInterface):
    
    def build(self, state: GraphState) -> GraphState:
        """
        Obtém o saldo do cliente.
        """

        logger.info("Node: Get Balance")

        state.balance.value = 750
        state.trace.append("get_balance")
        
        logger.info(f"Balance: {state.balance.value}")

        return state
