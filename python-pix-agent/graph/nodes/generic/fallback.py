from graph.graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

def fallback(state: GraphState) -> GraphState:
    logger.info("Node: Fallback")

    state.trace.append("fallback")

    return state
