from graph.graph_state import GraphState
from langgraph.graph import StateGraph, END
from langgraph.types import Interrupt
from langchain_core.runnables import RunnableLambda
from graph.nodes.llm.check_intention import CheckIntentionNodeStrategy
from graph.graphs.products import BalanceGraphFactory, GetLimitGraphFactory, UpdateLimitGraphFactory, PixGraph
from graph.graphs import FallbackGraph
from graph.nodes.generic.clean_state import CleanStateNodeStrategy

import json

from commons.logger import get_logger
logger = get_logger(__name__)

class MainGraph:
    def __init__(self):
        pass

    def build(self, message: str, state: GraphState = None) -> GraphState:
        """
        Gerencia o workflow do grafo.
        """
        logger.info("Criando MainGraph")
        
        # if state is None or CleanStateNodeStrategy.name() in state.trace:
        #     state = GraphState(user_message=message)

        # if state.intention:
        #     state.user_message = message
        #     state.intention = state.intention
        #     state.trace = []
        #     return self.create_workflow(state)
        # else:
        return self.create_workflow(state)

    # def continue_workflow(self, state: GraphState) -> GraphState:
    #     """
    #     Continua o workflow principal do grafo.
    #     """
        # router = self.build_router()
        # final_state = router.invoke(state)
        # return GraphState(**state)

    def create_workflow(self, state: GraphState) -> GraphState:
        """
        Cria o workflow principal do grafo.
        """
        graph_builder = StateGraph(GraphState)
        
        graph_builder.add_node(CheckIntentionNodeStrategy.name(), RunnableLambda(CheckIntentionNodeStrategy().build))
        graph_builder.add_node(BalanceGraphFactory.name(), RunnableLambda(BalanceGraphFactory().build))
        graph_builder.add_node(GetLimitGraphFactory.name(), RunnableLambda(GetLimitGraphFactory().build))
        graph_builder.add_node(UpdateLimitGraphFactory.name(), RunnableLambda(UpdateLimitGraphFactory().build))
        graph_builder.add_node(PixGraph.name(), RunnableLambda(PixGraph().build))
        graph_builder.add_node(FallbackGraph.name(), RunnableLambda(FallbackGraph().build))

        graph_builder.set_entry_point(CheckIntentionNodeStrategy.name())

        graph_builder.add_conditional_edges(
            CheckIntentionNodeStrategy.name(),
            self.decidir_proximo_no_depois_input,
            {
                BalanceGraphFactory.name(): BalanceGraphFactory.name(),
                GetLimitGraphFactory.name(): GetLimitGraphFactory.name(),
                UpdateLimitGraphFactory.name(): UpdateLimitGraphFactory.name(),
                FallbackGraph.name(): FallbackGraph.name(),
                PixGraph.name(): PixGraph.name(),
            }
        )

        graph = graph_builder.compile()

        events = graph.stream(state)
        
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

    @staticmethod
    def decidir_proximo_no_depois_input(state: GraphState) -> str:
        logger.info("================================================")
        logger.info(f"Intention: {state.intention}")
        logger.info("================================================")

        if state.intention == "consultar_limite":
            return GetLimitGraphFactory.name()

        elif state.intention == "alterar_limite":
            return UpdateLimitGraphFactory.name()

        elif state.intention == "consultar_saldo":
            return BalanceGraphFactory.name()

        elif state.intention == "realizar_pix":
            return PixGraph.name()

        else:
            return FallbackGraph.name()
