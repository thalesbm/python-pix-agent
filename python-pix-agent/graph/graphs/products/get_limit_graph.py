import asyncio
import threading

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.graph_state import GraphState
from graph.nodes.limits import get_limit
from utils.print_graph import print_graph
from graph.nodes.llm.format_answer_from_state import format_answer_from_state
from graph.nodes.generic.clean_state import clean_state

from logger import get_logger
logger = get_logger(__name__)

class GetLimitGraph:
    def __init__(self):
        pass

    def build(self):
        logger.info("Criando GetLimitGraph")

        graph_builder = StateGraph(GraphState)

        graph_builder.add_node("consultar_limite", RunnableLambda(get_limit))
        graph_builder.add_node("formatar_resposta", RunnableLambda(format_answer_from_state))
        graph_builder.add_node("limpar_estado", RunnableLambda(clean_state))
        
        graph_builder.set_entry_point("consultar_limite")
        graph_builder.add_edge("consultar_limite", "formatar_resposta") 
        graph_builder.add_edge("formatar_resposta", "limpar_estado") 
        graph_builder.add_edge("limpar_estado", END) 

        graph = graph_builder.compile()
        logger.info("GetLimitGraph criado")

        threading.Thread(target=lambda: asyncio.run(self.print(graph))).start()

        return graph

    async def print(self, graph):
        print_graph(graph, "get_limit")
