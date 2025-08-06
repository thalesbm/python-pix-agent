import asyncio
import threading

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.graph_state import GraphState
from graph.nodes.pix import check_value_key, simulate_pix, effective_pix, get_contact_pix, verify_date_pix
from graph.nodes.limits import get_limit
from graph.nodes.balance.get_balance import get_balance
from utils.print_graph import print_graph
from graph.nodes.receipt import receipt

from logger import get_logger
logger = get_logger(__name__)

class PixGraph:
    def __init__(self):
        pass

    def build(self):
        logger.info("Building graph")

        graph_builder = StateGraph(GraphState)

        graph_builder.add_node("verificar_chave_valor", RunnableLambda(check_value_key))
        graph_builder.add_node("simular_pix", RunnableLambda(simulate_pix))
        graph_builder.add_node("efetivar_pix", RunnableLambda(effective_pix))
        graph_builder.add_node("buscar_contato_pix", RunnableLambda(get_contact_pix))
        graph_builder.add_node("verificar_data_pix", RunnableLambda(verify_date_pix))
        graph_builder.add_node("consultar_limite", RunnableLambda(get_limit))
        graph_builder.add_node("saldo", RunnableLambda(get_balance))
        graph_builder.add_node("comprovante", RunnableLambda(receipt))

        graph_builder.set_entry_point("verificar_chave_valor")

        graph_builder.add_conditional_edges(
            "verificar_chave_valor",
            self.decidir_proximo_no_pix,
            {
                "saldo": "saldo",
                "verificar_data_pix": "verificar_data_pix",
            }
        )

        # Pix
        graph_builder.add_edge("verificar_data_pix", "saldo")
        graph_builder.add_edge("saldo", "consultar_limite")
        graph_builder.add_edge("consultar_limite", "buscar_contato_pix")
        graph_builder.add_edge("buscar_contato_pix", "simular_pix")
        graph_builder.add_edge("simular_pix", "efetivar_pix")
        graph_builder.add_edge("efetivar_pix", "comprovante")
        graph_builder.add_edge("comprovante", END)

        graph = graph_builder.compile()
        logger.info("Graph built")

        threading.Thread(target=lambda: asyncio.run(self.print(graph))).start()

        return graph

    @staticmethod
    def decidir_proximo_no_pix(state: GraphState) -> str:
        if state.intention == "realizar_pix":
            return "saldo"
        elif state.intention == "agendar_pix":
            return "verificar_data_pix"

    async def print(self, graph):
        name = "pix"
        logger.info("Printing graph: " + name)
        print_graph(graph, name)
        logger.info("Graph printed: " + name)