from graph.graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

def clean_state(state: GraphState) -> GraphState:
    logger.info("Node: CleanState")

    state.trace.append("clean_state")

    return state
