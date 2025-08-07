from graph.graph_state import GraphState

import time

from logger import get_logger
logger = get_logger(__name__)

def get_balance(state: GraphState) -> GraphState:
    logger.info("Node: Get Balance")
    
    time.sleep(1)
    
    state.balance.value = 750
    state.trace.append("get_balance")
    
    logger.info(f"Balance: {state.balance.value}")

    return state
