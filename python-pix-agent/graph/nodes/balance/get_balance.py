from graph.graph_state import GraphState

import time

from logger import get_logger
logger = get_logger(__name__)

def get_balance(state: GraphState) -> GraphState:
    logger.info("Node: Get Balance")
    
    time.sleep(1)
    
    state.balance.balance = 750
    
    logger.info(f"Balance: {state.balance.balance}")

    return state
