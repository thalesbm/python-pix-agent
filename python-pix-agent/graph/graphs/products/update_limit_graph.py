import asyncio
import threading

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.graph_state import GraphState
from graph.nodes.limits.verify_value import verify_limit_value
from graph.nodes.limits.update_limit import update_limit
from graph.nodes.receipt import receipt
from graph.nodes.llm.format_answer_from_state import format_answer_from_state
from graph.nodes.generic.clean_state import clean_state
from utils.print_graph import print_graph
from graph.nodes.generic.finish_simple_flow import finish_simple_flow

from logger import get_logger
logger = get_logger(__name__)

class UpdateLimitGraph:
    def __init__(self):
        pass

    def build(self):
        logger.info("Criando UpdateLimitGraph")

        graph_builder = StateGraph(GraphState)

        graph_builder.add_node("verificar_valor", RunnableLambda(verify_limit_value))
        graph_builder.add_node("atualizar_limite", RunnableLambda(update_limit))
        graph_builder.add_node("comprovante", RunnableLambda(receipt))
        graph_builder.add_node("formatar_resposta", RunnableLambda(format_answer_from_state))
        graph_builder.add_node("encerrar_fluxo_simples", RunnableLambda(finish_simple_flow))
        graph_builder.add_node("limpar_estado", RunnableLambda(clean_state))
        
        graph_builder.set_entry_point("verificar_valor")

        graph_builder.add_conditional_edges(
            "verificar_valor",
            self.decidir_proximo_no_limit,
            {
                "atualizar_limite": "atualizar_limite",
                "encerrar_fluxo_simples": "encerrar_fluxo_simples",
            }
        )

        graph_builder.add_edge("atualizar_limite", "comprovante")
        graph_builder.add_edge("comprovante", "formatar_resposta")
        graph_builder.add_edge("formatar_resposta", "limpar_estado")
        graph_builder.add_edge("limpar_estado", END)
        graph_builder.add_edge("encerrar_fluxo_simples", END)
        
        graph = graph_builder.compile()
        logger.info("UpdateLimitGraph criado")
        
        threading.Thread(target=lambda: asyncio.run(self.print(graph))).start()
        
        return graph

    @staticmethod
    def decidir_proximo_no_limit(state: GraphState) -> str:
        if state.limit.has_limit:
            return "atualizar_limite"
        else:
            return "encerrar_fluxo_simples"

    async def print(self, graph):
        print_graph(graph, "update_limit")
