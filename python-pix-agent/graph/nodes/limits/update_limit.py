from graph.graph_state import GraphState

import time

from logger import get_logger
logger = get_logger(__name__)

def update_limit(state: GraphState) -> GraphState:
    logger.info("Node: Update Limit")

    time.sleep(1)

    state.trace.append("update_limit")
    
    return state
