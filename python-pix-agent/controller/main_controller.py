from model.graph_state import GraphState
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.nodes.input_message import input_message
from graph.nodes.check_intention import check_intention
from graph.nodes.receipt import receipt
from utils.print_graph import print_graph   

class MainController:
    def __init__(self):
        pass

    def run(self, question: str):
        graph_builder = StateGraph(GraphState)

        graph_builder.add_node("input_message", RunnableLambda(input_message))
        graph_builder.add_node("check_intention", RunnableLambda(check_intention))
        graph_builder.add_node("receipt", RunnableLambda(receipt))

        graph_builder.set_entry_point("input_message")
        graph_builder.add_edge("input_message", "check_intention")
        graph_builder.add_edge("check_intention", "receipt")
        graph_builder.add_edge("receipt", END)

        graph = graph_builder.compile()

        print_graph(graph)