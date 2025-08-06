from graph_state import GraphState

import time

from logger import get_logger
logger = get_logger(__name__)

def receipt(state: GraphState) -> GraphState:
    logger.info("Node: Receipt")

    time.sleep(500)

    # Gera o comprovante
    state.receipt.receipt_id = "1234567890"

    return state
