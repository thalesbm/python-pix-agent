from graph.graph_state import GraphState
from langgraph.types import Interrupt
from functools import lru_cache
from graph.graphs import build_main_graph

import json

from commons.logger import get_logger
logger = get_logger(__name__)

class MainGraph:
    def __init__(self):
        pass

    def build(self, message: str, user_id: str) -> GraphState:
        """
        Cria o workflow principal do grafo.
        """
        logger.info(f"Iniciando grafo")
        logger.info(f"user_id: {user_id}")

        config = {
            "configurable": {
                "thread_id": f"user:{user_id}:conv:{user_id}"
            }
        }

        state = GraphState(user_message=message)

        events = build_main_graph().stream(state, config=config)
        
        for event in events:
            if "__interrupt__" in event:
                intr = event["__interrupt__"][0]
                new_state = self.interrupt_to_graph_state(intr, GraphState)

        logger.info("MainGraph criado")

        print("================================================")
        print(new_state)
        print("================================================")

        return new_state

    def interrupt_to_graph_state(self, intr: Interrupt, ModelCls):
        val = intr.value
        data = json.loads(val) if isinstance(val, str) else val
        state_dict = data.get("state", data)
        return ModelCls(**state_dict)
