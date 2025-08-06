from graph.graph_state import GraphState
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.nodes.receipt.receipt import receipt
from graph.nodes.pix.simulate_pix import simulate_pix
from graph.nodes.pix.effective_pix import effective_pix
from graph.nodes.pix.check_value_key import check_value_key
from graph.nodes.pix.get_contact_pix import get_contact_pix
from graph.nodes.pix.verify_date_pix import verify_date_pix
from graph.nodes.limits.update_limit import update_limit
from graph.nodes.limits.get_limit import get_limit
from graph.nodes.ask_more_information import ask_more_information
from graph.nodes.check_intention import check_intention
from graph.nodes.balance.get_balance import get_balance

from utils.print_graph import print_graph   
from typing import Literal

from logger import get_logger
logger = get_logger(__name__)

class MainController:
    def __init__(self):
        pass

    def run(self, message: str):
        logger.info(f"Mensagem recebida na MainController: {message}")

        graph_builder = StateGraph(GraphState)
        graph_builder.set_entry_point("verificar_intencao")

        graph_builder.add_node("verificar_intencao", RunnableLambda(check_intention))

        # Limites
        graph_builder.add_node("consultar_limite", RunnableLambda(get_limit))
        graph_builder.add_node("alterar_limite", RunnableLambda(update_limit))
        
        # Saldo
        graph_builder.add_node("saldo", RunnableLambda(get_balance))

        # Pix
        graph_builder.add_node("verificar_chave_valor", RunnableLambda(check_value_key))
        graph_builder.add_node("simular_pix", RunnableLambda(simulate_pix))
        graph_builder.add_node("efetivar_pix", RunnableLambda(effective_pix))
        graph_builder.add_node("buscar_contato_pix", RunnableLambda(get_contact_pix))
        graph_builder.add_node("verificar_data_pix", RunnableLambda(verify_date_pix))

        # Comprovantes
        graph_builder.add_node("comprovante", RunnableLambda(receipt))

        # Mais informações
        graph_builder.add_node("mais_informacoes", RunnableLambda(ask_more_information))

        graph_builder.add_conditional_edges(
            "verificar_intencao",
            lambda state: {
                "consultar_limite": "consultar_limite",
                "alterar_limite": "alterar_limite",
                "verificar_chave_valor": "verificar_chave_valor",
                "saldo": "saldo",
            }.get(state.intention.strip().lower(), "mais_informacoes"),
            {
                "consultar_limite": "consultar_limite",
                "alterar_limite": "alterar_limite",
                "verificar_chave_valor": "verificar_chave_valor",
                "saldo": "saldo",
                "mais_informacoes": "mais_informacoes",
            }
        )

        graph_builder.add_conditional_edges(
            "verificar_chave_valor",
            self.decidir_proximo_no,
            {
                "saldo": "saldo",
                "verificar_data_pix": "verificar_data_pix",
            }
        )

        graph_builder.add_edge("verificar_data_pix", "saldo")

        # Pix
        graph_builder.add_edge("saldo", "consultar_limite")
        graph_builder.add_edge("consultar_limite", "buscar_contato_pix")
        graph_builder.add_edge("buscar_contato_pix", "simular_pix")
        graph_builder.add_edge("simular_pix", "efetivar_pix")
        graph_builder.add_edge("efetivar_pix", "comprovante")
        graph_builder.add_edge("comprovante", END)

        # Limites
        graph_builder.add_edge("consultar_limite", END)
        graph_builder.add_edge("alterar_limite", "comprovante")
        
        # Saldo
        graph_builder.add_edge("saldo", END)

        # Comprovantes
        graph_builder.add_edge("comprovante", END)

        graph = graph_builder.compile()
        graph.invoke(GraphState(user_message=message))

        print_graph(graph)

    def decidir_proximo_no(state: GraphState) -> str:
        if state.intention == "realizar_pix":
            return "saldo"
        elif state.intention == "agendar_pix":
            return "verificar_data_pix"
