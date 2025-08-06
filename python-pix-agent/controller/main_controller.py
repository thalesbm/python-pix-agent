from graph.graph_state import GraphState
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.nodes.receipt.receipt import receipt
from graph.nodes.pix.scheduling_pix import scheduling_pix
from graph.nodes.pix.transaction_pix import transaction_pix
from graph.nodes.pix.check_value_key import check_value_key
from graph.nodes.pix.get_contact_pix import get_contact_pix
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
        graph_builder.add_node("transferir_pix", RunnableLambda(transaction_pix))
        graph_builder.add_node("agendar_pix", RunnableLambda(scheduling_pix))
        graph_builder.add_node("get_contact_pix", RunnableLambda(get_contact_pix))

        # Comprovantes
        graph_builder.add_node("comprovante", RunnableLambda(receipt))

        # Mais informações
        graph_builder.add_node("ask_more_information", RunnableLambda(ask_more_information))

        graph_builder.add_conditional_edges(
            "verificar_intencao",
            lambda state: {
                "consultar_limite": "consultar_limite",
                "alterar_limite": "alterar_limite",
                "saldo": "saldo",
            }.get(state.intention.strip().lower(), "ask_more_information"),
            {
                "consultar_limite": "consultar_limite",
                "alterar_limite": "alterar_limite",
                "saldo": "saldo",
                "ask_more_information": "ask_more_information",
            }
        )


        # graph_builder.add_conditional_edges(
        #     "check_intention",
        #     lambda state: {
        #         "consultar_limite": "consultar_limite",
        #         "alterar_limite": "alterar_limite",
        #         "realizar_pix": "verificar_chave_valor",
        #         "agendar_pix": "verificar_chave_valor",
        #     }.get(state.intention.strip().lower(), "ask_more_information"),
        #     {
        #         "consultar_limite": "consultar_limite",
        #         "alterar_limite": "alterar_limite",
        #         "realizar_pix": "verificar_chave_valor",
        #         "agendar_pix": "verificar_chave_valor",
        #         "ask_more_information": "ask_more_information",
        #     }
        # )

        # graph_builder.add_conditional_edges(
        #     "verificar_chave_valor",
        #     lambda state: (
        #         "transferir_pix" if state.intention == "realizar_pix" and state.tem_chave_valor
        #         else "agendar_pix" if state.intention == "agendar_pix" and state.tem_chave_valor
        #         else "ask_more_information"
        #     ),
        #     {
        #         "transferir_pix": "transferir_pix",
        #         "agendar_pix": "agendar_pix",
        #         "ask_more_information": "ask_more_information",
        #     }
        # )


        # Limites
        graph_builder.add_edge("consultar_limite", END)
        graph_builder.add_edge("alterar_limite", "comprovante")

        graph_builder.add_edge("transferir_pix", "comprovante")
        graph_builder.add_edge("agendar_pix", "comprovante")
        
        # Saldo
        graph_builder.add_edge("saldo", END)

        # Comprovantes
        graph_builder.add_edge("comprovante", END)

        graph = graph_builder.compile()
        graph.invoke(GraphState(user_message=message))

        print_graph(graph)
