from langchain_core.runnables.graph import MermaidDrawMethod
from datetime import datetime
from config import get_config

from logger import get_logger
logger = get_logger(__name__)

def print_graph(graph, name: str):
    """Imprime o grafo em formato de imagem."""

    config = get_config()

    if config.graph.print:
        """
        Imprime o grafo em formato de imagem.
        """
        logger.info("Imprimindo grafo")

        png_bytes = graph.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API
        )

        timestamp = int(datetime.now().timestamp())

        file_name = str(timestamp) + "_" + name + ".png"
        with open("files/" + file_name, "wb") as f:
            f.write(png_bytes)

        logger.info("Grafo impresso")
