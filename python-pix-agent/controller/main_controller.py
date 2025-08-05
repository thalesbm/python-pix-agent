from model.graph_state import GraphState
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.nodes.check_intention import check_intention
from graph.nodes.receipt import receipt
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
        graph_builder.add_node("receipt", RunnableLambda(receipt))

        graph_builder.set_entry_point("check_intention")

        graph_builder.add_conditional_edges(
            "check_intention",
            self.decidir_proximo_no,
            {
                "check_limit": "check_limit",
                "scheduling_pix": "scheduling_pix",
                "transaction_pix": "transaction_pix",
                "fallback": "fallback",
            }
        )

        graph_builder.add_edge(self.decidir_proximo_no, "receipt")

        graph_builder.add_edge("receipt", END)

        graph = graph_builder.compile()
        graph.invoke(GraphState(user_message=message))

        print_graph(graph)

    def decidir_proximo_no(self, state: GraphState) -> str:
        intention = state.intention.strip().lower()
        if intention == "consultar_limite":
            return "check_limit"

        elif intention == "agendar_pix":
            return "scheduling_pix"

        elif intention == "realizar_pix":
            return "transaction_pix"

        else:
            return "fallback"