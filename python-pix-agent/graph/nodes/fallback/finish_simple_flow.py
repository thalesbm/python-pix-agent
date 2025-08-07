from graph.graph_state import GraphState

from logger import get_logger
logger = get_logger(__name__)

def finish_simple_flow(state: GraphState) -> GraphState:
    logger.info("Node: Finish Simple Flow")

    state.trace.append("finish_simple_flow")

    return state
