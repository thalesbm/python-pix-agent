import asyncio
import threading

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.graph_state import GraphState
from graph.nodes.balance.get_balance import get_balance
from utils.print_graph import print_graph
from graph.nodes.llm.format_answer_from_state import format_answer_from_state

from logger import get_logger
logger = get_logger(__name__)

class BalanceGraph:
    def __init__(self):
        pass

    def build(self):    
        logger.info("Criando BalanceGraph")
        
        graph_builder = StateGraph(GraphState)

        graph_builder.add_node("saldo", RunnableLambda(get_balance))
        graph_builder.add_node("formatar_resposta", RunnableLambda(format_answer_from_state))
        graph_builder.set_entry_point("saldo")
        
        graph_builder.add_edge("saldo", "formatar_resposta")
        graph_builder.add_edge("formatar_resposta", END)

        graph = graph_builder.compile()
        logger.info("BalanceGraph criado")

        threading.Thread(target=lambda: asyncio.run(self.print(graph))).start()

        return graph

    async def print(self, graph):
        print_graph(graph, "balance")
