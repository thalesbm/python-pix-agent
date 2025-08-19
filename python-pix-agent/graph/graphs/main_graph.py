from graph.graph_state import GraphState
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda, RunnableBranch
from graph.nodes.llm.check_intention import CheckIntentionNodeStrategy
from graph.graphs.products import BalanceGraphFactory, GetLimitGraphFactory, UpdateLimitGraphFactory, PixGraph
from graph.graphs import FallbackGraph
from graph.nodes.generic.clean_state import CleanStateNodeStrategy

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
        logger.info("Criando MainGraph")
        
        if state is None or CleanStateNodeStrategy.name() in state.trace:
            state = GraphState(user_message=message)

        if state.intention:
            state.user_message = message
            state.intention = state.intention
            state.trace = []
            return self.continue_workflow(state)
        else:
            return self.create_workflow(state)

    def continue_workflow(self, state: GraphState) -> GraphState:
        """
        Continua o workflow principal do grafo.
        """
        router = self.build_router()
        final_state = router.invoke(state)
        return GraphState(**final_state)

    def create_workflow(self, state: GraphState) -> GraphState:
        """
        Cria o workflow principal do grafo.
        """
        graph_builder = StateGraph(GraphState)

        router = self.build_router()
        
        graph_builder.add_node(CheckIntentionNodeStrategy.name(), RunnableLambda(CheckIntentionNodeStrategy().build))
        graph_builder.add_node("router", router)

        graph_builder.set_entry_point(CheckIntentionNodeStrategy.name())

        graph_builder.add_edge(CheckIntentionNodeStrategy.name(), "router")

        graph = graph_builder.compile()

        steps = graph.invoke(state, stream=True)

        print("Tipo de steps:", type(steps))
        print("Tipo de steps:", steps)

        # for step in steps:
            # if step["type"] == "interrupt":
                # print("interrupt")
                # print(step["content"]["message"])
            # elif step["type"] == "end":
                # final_state = GraphState(**step["data"])
        
        final_state = GraphState(**steps)

        logger.info("MainGraph criado")

        return final_state

    def build_router(self):
        """
            O router é responsável por direcionar o fluxo do grafo com base na intenção do usuário.
        """
        saldo_graph = BalanceGraphFactory().build()
        get_limite_graph = GetLimitGraphFactory().build()
        update_limit_graph = UpdateLimitGraphFactory().build()
        pix_graph = PixGraph().build()
        fallback_graph = FallbackGraph().build()

        router = RunnableBranch(
            (lambda state: state.intention == "consultar_limite", get_limite_graph),
            (lambda state: state.intention == "alterar_limite", update_limit_graph),
            (lambda state: state.intention == "consultar_saldo", saldo_graph),
            (lambda state: state.intention == "realizar_pix", pix_graph),
            fallback_graph
        )

        return router
