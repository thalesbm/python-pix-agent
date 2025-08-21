from graph.graph_state import GraphState
from langgraph.types import Interrupt
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

        initial_state = GraphState(user_message=message)

        events = build_main_graph().stream(
            initial_state, 
            config=self.get_config(user_id)
        )

        logger.info("Grafo compilado, salvo e executado")
        
        last_state: GraphState = initial_state

        for event in events:
            if "__interrupt__" in event:
                intr = event["__interrupt__"][0]
                return self.interrupt_to_graph_state(intr, GraphState)

        payload = next(iter(event.values()))

        if isinstance(payload, GraphState):
            last_state = payload
        elif isinstance(payload, dict):
            last_state = GraphState(**payload)
        else:
            logger.debug(f"Evento inesperado: {type(payload)}")

        print("================================================")
        print(last_state)
        print("================================================")

        return last_state

    def get_config(self, user_id: str) -> dict:
        return {
            "configurable": {
                "thread_id": f"user:{user_id}:conv:{user_id}"
            }
        }

    def interrupt_to_graph_state(self, intr: Interrupt, ModelCls):
        val = intr.value
        data = json.loads(val) if isinstance(val, str) else val
        state_dict = data.get("state", data)
        return ModelCls(**state_dict)
