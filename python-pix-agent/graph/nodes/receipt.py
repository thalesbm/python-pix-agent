from model.graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

def receipt(state: GraphState) -> GraphState:
    logger.info(f"Recebendo o estado: {state}")
    
    state.receipt = "O Comprovante foi gerado com sucesso!"
    return state
