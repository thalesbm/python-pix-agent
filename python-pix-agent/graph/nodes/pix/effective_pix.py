from graph.graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

def effective_pix(state: GraphState) -> GraphState:
    logger.info("Node: Effective Pix")

    state.trace.append("effective_pix")

    return state
