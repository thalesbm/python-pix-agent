from model.graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

def check_limit(state: GraphState) -> GraphState:
    logger.info("Node: Check Limit")
    
    return state
