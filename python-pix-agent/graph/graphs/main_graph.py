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
            return self.create_workflow(state)
        else:
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

        # router = self.build_router()
        
        graph_builder.add_node(CheckIntentionNodeStrategy.name(), RunnableLambda(CheckIntentionNodeStrategy().build))
        graph_builder.add_node(BalanceGraphFactory.name(), RunnableLambda(BalanceGraphFactory().build))
        graph_builder.add_node(GetLimitGraphFactory.name(), RunnableLambda(GetLimitGraphFactory().build))
        graph_builder.add_node(UpdateLimitGraphFactory.name(), RunnableLambda(UpdateLimitGraphFactory().build))
        graph_builder.add_node(PixGraph.name(), RunnableLambda(PixGraph().build))
        graph_builder.add_node(FallbackGraph.name(), RunnableLambda(FallbackGraph().build))

        graph_builder.set_entry_point(CheckIntentionNodeStrategy.name())

        # graph_builder.add_edge(CheckIntentionNodeStrategy.name(), BalanceGraphFactory.name())
        # graph_builder.add_edge(CheckIntentionNodeStrategy.name(), GetLimitGraphFactory.name())
        # graph_builder.add_edge(CheckIntentionNodeStrategy.name(), UpdateLimitGraphFactory.name())
        # graph_builder.add_edge(CheckIntentionNodeStrategy.name(), PixGraph.name())
        # graph_builder.add_edge(CheckIntentionNodeStrategy.name(), FallbackGraph.name())

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

        final_state = graph_builder.compile().invoke(state)

        # steps = graph.stream(state)

        # print(type(steps))
        # print(steps)

        # for step in steps:
        #     print("📦 step:", step)
        #     if "__interrupt__" in step:
        #         intr = step["__interrupt__"][0]
        #         print("🚫 Interrompido com:", intr.value["message"])

        # final_state = GraphState(**graph)

        logger.info("MainGraph criado")

        # print("================================================")
        # print(type(final_state))
        # print(final_state)
        # print("================================================")

        return final_state

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

    # def build_router(self):
    #     """
    #         O router é responsável por direcionar o fluxo do grafo com base na intenção do usuário.
    #     """
    #     saldo_graph = BalanceGraphFactory().build()
    #     get_limite_graph = GetLimitGraphFactory().build()
    #     update_limit_graph = UpdateLimitGraphFactory().build()
    #     pix_graph = PixGraph().build()
    #     fallback_graph = FallbackGraph().build()

    #     router = RunnableBranch(
    #         (lambda state: state.intention == "consultar_limite", get_limite_graph),
    #         (lambda state: state.intention == "alterar_limite", update_limit_graph),
    #         (lambda state: state.intention == "consultar_saldo", saldo_graph),
    #         (lambda state: state.intention == "realizar_pix", pix_graph),
    #         fallback_graph
    #     )

    #     return router
