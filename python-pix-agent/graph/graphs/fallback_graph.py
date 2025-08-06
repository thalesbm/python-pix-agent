import asyncio
import threading

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.graph_state import GraphState
from graph.nodes.fallback.fallback import fallback
from utils.print_graph import print_graph

from logger import get_logger
logger = get_logger(__name__)

class FallbackGraph:
    def __init__(self):
        pass

    def build(self):    
        logger.info("Building graph")
        
        graph_builder = StateGraph(GraphState)

        graph_builder.add_node("fallback", RunnableLambda(fallback))
        graph_builder.set_entry_point("fallback")
        graph_builder.add_edge("fallback", END)

        graph = graph_builder.compile()
        logger.info("Graph built")

        threading.Thread(target=lambda: asyncio.run(self.print(graph))).start()

        return graph

    async def print(self, graph):
        name = "fallback"
        logger.info("Printing graph: " + name)
        print_graph(graph, name)
        logger.info("Graph printed: " + name)
