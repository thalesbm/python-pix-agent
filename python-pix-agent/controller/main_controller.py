from model.graph_state import GraphState
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.nodes.check_intention import check_intention
from graph.nodes.receipt import receipt
from utils.print_graph import print_graph   

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
        graph_builder.add_edge("check_intention", "receipt")
        graph_builder.add_edge("receipt", END)

        graph = graph_builder.compile()
        graph.invoke(GraphState(user_message=message))

        print_graph(graph)