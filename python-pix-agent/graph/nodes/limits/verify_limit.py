from model.graph_state import GraphState

import time

from logger import get_logger
logger = get_logger(__name__)

def verify_limit(state: GraphState) -> GraphState:
    logger.info("Node: Verify Limit")

    # Busca o limite do cliente na base:    
    state.limit = 1000
    time.sleep(1)

    # Verifica se o limite é suficiente:
    if state.limit >= state.value:
        state.answer = "Limite suficiente"
    else:
        state.answer = "Limite insuficiente"
    
    return state
