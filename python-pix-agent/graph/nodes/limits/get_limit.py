from graph.graph_state import GraphState

import time

from logger import get_logger
logger = get_logger(__name__)

def get_limit(state: GraphState) -> GraphState:
    logger.info("Node: Get Limit")
    
    time.sleep(1)
    
    state.limit.limit = 1000
    
    return state
