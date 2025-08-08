import asyncio
import threading

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.graph_state import GraphState
from graph.nodes.balance.get_balance import GetBalanceNodeStrategy
from graph.nodes.llm.format_answer_from_state import FormatAnswerFromStateNodeStrategy
from graph.nodes.generic.clean_state import CleanStateNodeStrategy

from utils.print_graph import print_graph

from logger import get_logger
logger = get_logger(__name__)

class BalanceGraph:
    def __init__(self):
        pass

    def build(self):    
        logger.info("Criando BalanceGraph")
        
        graph_builder = StateGraph(GraphState)

        graph_builder.add_node("saldo", RunnableLambda(GetBalanceNodeStrategy().build))
        graph_builder.add_node("formatar_resposta", RunnableLambda(FormatAnswerFromStateNodeStrategy().build))
        graph_builder.add_node("limpar_estado", RunnableLambda(CleanStateNodeStrategy().build))
        
        graph_builder.set_entry_point("saldo")
        
        graph_builder.add_edge("saldo", "formatar_resposta")
        graph_builder.add_edge("formatar_resposta", "limpar_estado")
        graph_builder.add_edge("limpar_estado", END)

        graph = graph_builder.compile()
        logger.info("BalanceGraph criado")

        threading.Thread(target=lambda: asyncio.run(self.print(graph))).start()

        return graph

    async def print(self, graph):
        print_graph(graph, "balance")
