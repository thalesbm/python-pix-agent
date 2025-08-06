from graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

def ask_more_information(state: GraphState) -> GraphState:
    logger.info("Node: Ask More Information")
    return state
