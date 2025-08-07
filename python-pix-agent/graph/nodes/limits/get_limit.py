from graph.graph_state import GraphState

from datetime import datetime

from logger import get_logger
logger = get_logger(__name__)

def get_limit(state: GraphState) -> GraphState:
    logger.info("Node: Get Limit")

    state.limit.value = 1000
    state.limit.last_update = datetime.now()
    state.trace.append("get_limit")
    
    return state
