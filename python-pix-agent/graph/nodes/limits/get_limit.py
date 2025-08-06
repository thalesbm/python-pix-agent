from graph.graph_state import GraphState

import time
from datetime import datetime

from logger import get_logger
logger = get_logger(__name__)

def get_limit(state: GraphState) -> GraphState:
    logger.info("Node: Get Limit")
    
    time.sleep(1)
    
    state.limit.value = 1000
    state.limit.last_update = datetime.now()
    
    return state
