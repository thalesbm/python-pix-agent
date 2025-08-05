from model.graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

def transaction_pix(state: GraphState) -> GraphState:
    logger.info("Node: Transaction Pix")
    return state
