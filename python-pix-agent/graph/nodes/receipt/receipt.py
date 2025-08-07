from graph.graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

def receipt(state: GraphState) -> GraphState:
    logger.info("Node: Receipt iniciado")

    state.receipt.receipt_id = "1234567890"
    state.trace.append("receipt")

    logger.info("Node: Receipt finalizado")

    return state
