import asyncio
import threading

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.graph_state import GraphState
from graph.nodes.limits import update_limit
from graph.nodes.receipt import receipt
from utils.print_graph import print_graph

from logger import get_logger
logger = get_logger(__name__)

class UpdateLimitGraph:
    def __init__(self):
        pass

    def build(self):
        logger.info("Building graph")

        graph_builder = StateGraph(GraphState)

        graph_builder.add_node("alterar_limite", RunnableLambda(update_limit))
        graph_builder.add_node("comprovante", RunnableLambda(receipt))
        
        graph_builder.set_entry_point("alterar_limite")
        graph_builder.add_edge("alterar_limite", "comprovante")
        graph_builder.add_edge("comprovante", END)
        
        graph = graph_builder.compile()
        logger.info("Graph built")
        
        threading.Thread(target=lambda: asyncio.run(self.print(graph))).start()
        
        return graph

    async def print(self, graph):
        name = "update_limit"
        logger.info("Printing graph: " + name)
        print_graph(graph, name)
        logger.info("Graph printed: " + name)
