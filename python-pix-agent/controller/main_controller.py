from model import GraphState
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.graph import MermaidDrawMethod
from graph.nodes.input_message import input_message
from graph.nodes.check_intention import check_intention
from graph.nodes.receipt import receipt

class MainController:
    def __init__(self):
        pass

    def run(self):
        graph_builder = StateGraph(GraphState)

        graph_builder.add_node("input_message", RunnableLambda(input_message))
        graph_builder.add_node("check_intention", RunnableLambda(check_intention))
        graph_builder.add_node("receipt", RunnableLambda(receipt))

        graph_builder.set_entry_point("input_message")
        graph_builder.add_edge("input_message", "check_intention")
        graph_builder.add_edge("check_intention", "welcome")

        graph = graph_builder.compile()

        png_bytes = graph.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API
        )
        with open("files/grafo_exemplo1.png", "wb") as f:
            f.write(png_bytes)