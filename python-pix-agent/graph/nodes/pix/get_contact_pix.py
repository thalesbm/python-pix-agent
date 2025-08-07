from graph.graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

def get_contact_pix(state: GraphState) -> GraphState:
    logger.info("Node: Get Contact Pix")

    state.trace.append("get_contact_pix")

    return state
