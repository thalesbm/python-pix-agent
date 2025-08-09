import asyncio
import threading

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.graph_state import GraphState
from graph.nodes.pix.check_value_key import CheckValueKeyNodeStrategy
from graph.nodes.pix.simulate_pix import SimulatePixNodeStrategy
from graph.nodes.pix.effective_pix import EffectivePixNodeStrategy
from graph.nodes.pix.get_contact_pix import GetContactPixNodeStrategy
from graph.nodes.pix.verify_date_pix import VerifyDatePixNodeStrategy
from graph.nodes.limits.get_limit import GetLimitNodeStrategy
from graph.nodes.balance.get_balance import GetBalanceNodeStrategy
from graph.nodes.receipt.receipt import ReceiptNodeStrategy
from graph.nodes.generic.finish_simple_flow import FinishSimpleFlowNodeStrategy
from graph.nodes.llm.format_answer_from_state import FormatAnswerFromStateNodeStrategy
from graph.nodes.generic.clean_state import CleanStateNodeStrategy

from utils.print_graph import print_graph

from logger import get_logger
logger = get_logger(__name__)

class PixGraph:
    def __init__(self):
        pass

    def build(self):
        """
        Cria o workflow de pix do grafo.
        """
        logger.info("Criando PixGraph")

        graph_builder = StateGraph(GraphState)

        graph_builder.add_node("verificar_chave_valor", RunnableLambda(CheckValueKeyNodeStrategy().build))
        graph_builder.add_node("simular_pix", RunnableLambda(SimulatePixNodeStrategy().build))
        graph_builder.add_node("efetivar_pix", RunnableLambda(EffectivePixNodeStrategy().build))
        graph_builder.add_node("buscar_contato_pix", RunnableLambda(GetContactPixNodeStrategy().build))
        graph_builder.add_node("verificar_data_pix", RunnableLambda(VerifyDatePixNodeStrategy().build))
        graph_builder.add_node("consultar_limite", RunnableLambda(GetLimitNodeStrategy().build))
        graph_builder.add_node("saldo", RunnableLambda(GetBalanceNodeStrategy().build))
        graph_builder.add_node("comprovante", RunnableLambda(ReceiptNodeStrategy().build))
        graph_builder.add_node("encerrar_fluxo_simples", RunnableLambda(FinishSimpleFlowNodeStrategy().build))
        graph_builder.add_node("formatar_resposta", RunnableLambda(FormatAnswerFromStateNodeStrategy().build))
        graph_builder.add_node("limpar_estado", RunnableLambda(CleanStateNodeStrategy().build))

        graph_builder.set_entry_point("verificar_chave_valor")

        graph_builder.add_conditional_edges(
            "verificar_chave_valor",
            self.decidir_proximo_no_depois_input,
            {
                "saldo": "saldo",
                "encerrar_fluxo_simples": "encerrar_fluxo_simples",
            }
        )

        # Pix
        graph_builder.add_edge("verificar_data_pix", "saldo")
        graph_builder.add_edge("saldo", "consultar_limite")
        graph_builder.add_edge("consultar_limite", "buscar_contato_pix")
        graph_builder.add_edge("buscar_contato_pix", "simular_pix")
        graph_builder.add_edge("simular_pix", "efetivar_pix")
        graph_builder.add_edge("efetivar_pix", "comprovante")
        graph_builder.add_edge("comprovante", "formatar_resposta")
        graph_builder.add_edge("formatar_resposta", "limpar_estado")
        graph_builder.add_edge("limpar_estado", END)
        graph_builder.add_edge("encerrar_fluxo_simples", END)

        graph = graph_builder.compile()
        logger.info("PixGraph criado")

        threading.Thread(target=lambda: asyncio.run(self.print(graph))).start()

        return graph

    @staticmethod
    def decidir_proximo_no_depois_input(state: GraphState) -> str:
        logger.info("================================================")
        logger.info(f"Value: {state.pix.has_value}")
        logger.info(f"Key: {state.pix.has_key}")
        logger.info("================================================")

        if state.pix.has_value and state.pix.has_key:
            return "saldo"
        else:
            return "encerrar_fluxo_simples"

    async def print(self, graph):
        print_graph(graph, "pix")
