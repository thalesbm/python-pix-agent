from graph.graph_state import GraphState

from datetime import datetime

from logger import get_logger
logger = get_logger(__name__)

def update_limit(state: GraphState) -> GraphState:
    logger.info("Node: Update Limit")

    state.limit.value = 2500
    state.limit.last_update = datetime.now()

    state.trace.append("update_limit")
    
    return state
