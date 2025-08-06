from model.graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

def get_contact(state: GraphState) -> GraphState:
    logger.info("Node: Get Contact")
    return state
