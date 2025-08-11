from graph.graph_state import GraphState
from graph.nodes.graph_strategy_interface import GraphStrategyInterface

from logger import get_logger
logger = get_logger(__name__)

class GetBalanceNodeStrategy(GraphStrategyInterface):
    
    def name() -> str:
        return "get_balance"
    
    def build(self, state: GraphState) -> GraphState:
        """
        Obtém o saldo do cliente.
        """
        super().build(state) 

        logger.info("Node: Get Balance")

        state.balance.value = 750 
        
        logger.info(f"Balance: {state.balance.value}")

        return state
