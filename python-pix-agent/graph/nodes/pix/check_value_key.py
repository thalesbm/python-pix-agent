from graph.graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

def check_value_key(state: GraphState) -> GraphState:
    logger.info("Node: Check Value Key")

    state.trace.append("check_value_key")

    return state
