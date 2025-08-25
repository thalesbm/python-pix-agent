from graph.state.graph_state import GraphState
from langgraph.types import Interrupt
from graph.graphs import build_main_graph
from graph.graphs.checkpointer import CHECKPOINT_DB
from langgraph.checkpoint.sqlite import SqliteSaver
from commons.session.session_store import SessionStore          # ✅ seu store custom

import json

from commons.logger import get_logger
logger = get_logger(__name__)

class MainGraph:
    def __init__(self):
        self.store = SessionStore(CHECKPOINT_DB)

    def build(self, message: str, user_id: str) -> GraphState:
        """
        Cria o workflow principal do grafo.
        """
        logger.info(f"Iniciando grafo")

        cfg = self.get_config(user_id)
        thread_id = cfg["configurable"]["thread_id"]

        waiting, _last_prompt = self.store.get_waiting(thread_id)
        if waiting:
            logger.info(f"Iniciando grafo com user_message: {message} (interrupt)")
            input_for_graph = message
        else:
            logger.info(f"Iniciando grafo com user_message: {message} (normal)")
            input_for_graph = GraphState(user_message=message)

        # initial_state = GraphState(user_message=message)

        events = build_main_graph().stream(
            input_for_graph, 
            config=cfg
        )

        logger.info("Grafo compilado, salvo e executado")
        
        # last_state: GraphState = input_for_graph

        for event in events:
            if "__interrupt__" in event:
                intr = event["__interrupt__"][0]
                print("================================================")
                print(intr)
                print("================================================")
                return self.interrupt_to_graph_state(intr, GraphState)

        payload = next(iter(event.values()))

        if isinstance(payload, GraphState):
            input_for_graph = payload
        elif isinstance(payload, dict):
            input_for_graph = GraphState(**payload)
        else:
            logger.debug(f"Evento inesperado: {type(payload)}")

        self.store.set_waiting(thread_id, False, None)

        print("================================================")
        print(input_for_graph)
        print("================================================")

        return input_for_graph

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
