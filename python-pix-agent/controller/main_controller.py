from model.graph_state import GraphState
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.nodes.check_intention import check_intention
from graph.nodes.receipt import receipt
from graph.nodes.scheduling_pix import scheduling_pix
from graph.nodes.transaction_pix import transaction_pix
from graph.nodes.check_limit import check_limit
from graph.nodes.check_value_key import check_value_key
from graph.nodes.fallback import fallback
from graph.nodes.ask_more_information import ask_more_information
from graph.nodes.update_limit import update_limit
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

        graph_builder.add_node("check_intention", RunnableLambda(check_intention))
        graph_builder.add_node("consultar_limite", RunnableLambda(check_limit))
        graph_builder.add_node("alterar_limite", RunnableLambda(update_limit))
        graph_builder.add_node("verificar_chave_valor", RunnableLambda(check_value_key))
        graph_builder.add_node("transferir_pix", RunnableLambda(transaction_pix))
        graph_builder.add_node("agendar_pix", RunnableLambda(scheduling_pix))
        graph_builder.add_node("receipt", RunnableLambda(receipt))
        graph_builder.add_node("ask_more_information", RunnableLambda(ask_more_information))

        graph_builder.set_entry_point("check_intention")
        
        graph_builder.add_conditional_edges(
            "check_intention",
            lambda state: {
                "consultar_limite": "consultar_limite",
                "alterar_limite": "alterar_limite",
                "realizar_pix": "verificar_chave_valor",
                "agendar_pix": "verificar_chave_valor",
            }.get(state.intention.strip().lower(), "ask_more_information"),
            {
                "consultar_limite": "consultar_limite",
                "alterar_limite": "alterar_limite",
                "realizar_pix": "verificar_chave_valor",
                "agendar_pix": "verificar_chave_valor",
                "ask_more_information": "ask_more_information",
            }
        )

        graph_builder.add_conditional_edges(
            "verificar_chave_valor",
            lambda state: (
                "transferir_pix" if state.intention == "realizar_pix" and state.tem_chave_valor
                else "agendar_pix" if state.intention == "agendar_pix" and state.tem_chave_valor
                else "ask_more_information"
            ),
            {
                "transferir_pix": "transferir_pix",
                "agendar_pix": "agendar_pix",
                "ask_more_information": "ask_more_information",
            }
        )

        graph_builder.add_edge("transferir_pix", "receipt")
        graph_builder.add_edge("agendar_pix", "receipt")
        graph_builder.add_edge("consultar_limite", END)
        graph_builder.add_edge("alterar_limite", "receipt")
        graph_builder.add_edge("receipt", END)

        graph = graph_builder.compile()
        graph.invoke(GraphState(user_message=message))

        print_graph(graph)
