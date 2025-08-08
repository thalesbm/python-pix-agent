import asyncio
import threading

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.graph_state import GraphState
from graph.nodes.limits.verify_value import VerifyLimitValueNodeStrategy
from graph.nodes.limits.update_limit import UpdateLimitNodeStrategy
from graph.nodes.receipt.receipt import ReceiptNodeStrategy
from graph.nodes.llm.format_answer_from_state import FormatAnswerFromStateNodeStrategy
from graph.nodes.generic.clean_state import CleanStateNodeStrategy
from graph.nodes.generic.finish_simple_flow import FinishSimpleFlowNodeStrategy

from utils.print_graph import print_graph

from logger import get_logger
logger = get_logger(__name__)

class UpdateLimitGraph:
    def __init__(self):
        pass

    def build(self):
        logger.info("Criando UpdateLimitGraph")

        graph_builder = StateGraph(GraphState)

        graph_builder.add_node("verificar_valor", RunnableLambda(VerifyLimitValueNodeStrategy().build))
        graph_builder.add_node("atualizar_limite", RunnableLambda(UpdateLimitNodeStrategy().build))
        graph_builder.add_node("comprovante", RunnableLambda(ReceiptNodeStrategy().build))
        graph_builder.add_node("formatar_resposta", RunnableLambda(FormatAnswerFromStateNodeStrategy().build))
        graph_builder.add_node("encerrar_fluxo_simples", RunnableLambda(FinishSimpleFlowNodeStrategy().build))
        graph_builder.add_node("limpar_estado", RunnableLambda(CleanStateNodeStrategy().build))
        
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
