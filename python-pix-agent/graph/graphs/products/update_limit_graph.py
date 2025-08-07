import asyncio
import threading

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.graph_state import GraphState
from graph.nodes.limits.verify_value import verify_value
from graph.nodes.limits.update_limit import update_limit
from graph.nodes.receipt import receipt
from graph.nodes.llm.format_answer_from_state import format_answer_from_state
from utils.print_graph import print_graph   

from logger import get_logger
logger = get_logger(__name__)

class UpdateLimitGraph:
    def __init__(self):
        pass

    def build(self):
        logger.info("Criando UpdateLimitGraph")

        graph_builder = StateGraph(GraphState)

        graph_builder.add_node("verificar_valor", RunnableLambda(verify_value))
        graph_builder.add_node("atualizar_limite", RunnableLambda(update_limit))
        graph_builder.add_node("comprovante", RunnableLambda(receipt))
        graph_builder.add_node("formatar_resposta", RunnableLambda(format_answer_from_state))
        
        graph_builder.set_entry_point("verificar_valor")

        graph_builder.add_conditional_edges(
            "verificar_valor",
            self.decidir_proximo_no_limit,
            {
                "atualizar_limite": "atualizar_limite",
                "formatar_resposta": "formatar_resposta",
            }
        )

        graph_builder.add_edge("atualizar_limite", "comprovante")
        graph_builder.add_edge("comprovante", "formatar_resposta")
        graph_builder.add_edge("formatar_resposta", END)
        
        graph = graph_builder.compile()
        logger.info("UpdateLimitGraph criado")
        
        threading.Thread(target=lambda: asyncio.run(self.print(graph))).start()
        
        return graph

    @staticmethod
    def decidir_proximo_no_limit(state: GraphState) -> str:
        if state.limit.value:
            return "atualizar_limite"
        else:
            return "formatar_resposta"

    async def print(self, graph):
        print_graph(graph, "update_limit")
