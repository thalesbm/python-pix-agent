from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.graph_state import GraphState
from graph.nodes.generic.fallback import FallbackNodeStrategy
from commons.utils.print_graph import config_print_graph

from commons.logger import get_logger
logger = get_logger(__name__)

class FallbackGraph:
    def __init__(self):
        pass

    def build(self):
        """
        Cria o workflow de fallback do grafo.
        """
        logger.info("Criando FallbackGraph")
        
        graph_builder = StateGraph(GraphState)

        graph_builder.add_node(FallbackNodeStrategy.name(), RunnableLambda(FallbackNodeStrategy().build))
        graph_builder.set_entry_point(FallbackNodeStrategy.name())
        graph_builder.add_edge(FallbackNodeStrategy.name(), END)

        graph = graph_builder.compile()
        logger.info("FallbackGraph criado")

        config_print_graph(graph, "fallback")

        return graph
