from graph.graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

def get_balance(state: GraphState) -> GraphState:
    logger.info("Node: Get Balance")

    state.balance.value = 750
    state.trace.append("get_balance")
    
    logger.info(f"Balance: {state.balance.value}")

    return state
