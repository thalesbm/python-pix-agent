from graph.state.graph_state import GraphState
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from graph.nodes.llm.check_intention import CheckIntentionNodeStrategy
from graph.graphs.products import BalanceGraphFactory, GetLimitGraphFactory, UpdateLimitGraphFactory, PixGraph
from graph.graphs import FallbackGraph
from graph.graphs.checkpointer import get_saver
from functools import lru_cache     
from langchain_core.runnables import Runnable

from commons.logger import get_logger
logger = get_logger(__name__)

@lru_cache(maxsize=1)
def build_main_graph() -> Runnable:
    """
    Compila o grafo principal.
    """

    logger.info("Criando grafo principal")

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
        decidir_proximo_no_depois_input,
        {
            BalanceGraphFactory.name(): BalanceGraphFactory.name(),
            GetLimitGraphFactory.name(): GetLimitGraphFactory.name(),
            UpdateLimitGraphFactory.name(): UpdateLimitGraphFactory.name(),
            FallbackGraph.name(): FallbackGraph.name(),
            PixGraph.name(): PixGraph.name(),
        }
    )

    logger.info("Grafo principal criado")

    return graph_builder.compile(checkpointer=get_saver())

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
