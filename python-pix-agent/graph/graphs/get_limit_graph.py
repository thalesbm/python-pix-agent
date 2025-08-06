import asyncio
import threading

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.graph_state import GraphState
from graph.nodes.limits import get_limit
from utils.print_graph import print_graph

from logger import get_logger
logger = get_logger(__name__)

class GetLimitGraph:
    def __init__(self):
        pass

    def build(self):
        logger.info("Building graph")

        graph_builder = StateGraph(GraphState)

        graph_builder.add_node("consultar_limite", RunnableLambda(get_limit))
        
        graph_builder.set_entry_point("consultar_limite")
        graph_builder.add_edge("consultar_limite", END)

        graph = graph_builder.compile()
        logger.info("Graph built")

        threading.Thread(target=lambda: asyncio.run(self.print(graph))).start()

        return graph

    async def print(self, graph):
        name = "get_limit"
        logger.info("Printing graph: " + name)
        print_graph(graph, name)
        logger.info("Graph printed: " + name)