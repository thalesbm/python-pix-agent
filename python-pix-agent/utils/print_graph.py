from langchain_core.runnables.graph import MermaidDrawMethod
from datetime import datetime

def print_graph(graph, name: str) -> int:
    """Imprime o grafo em formato de imagem."""

    png_bytes = graph.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.API
    )

    timestamp = int(datetime.now().timestamp())

    with open("files/" + name + "-" + str(timestamp) + ".png", "wb") as f:
        f.write(png_bytes)

    return timestamp
