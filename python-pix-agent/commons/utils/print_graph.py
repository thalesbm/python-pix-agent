import asyncio
import threading

from langchain_core.runnables.graph import MermaidDrawMethod
from datetime import datetime
from config import get_config

from commons.logger import get_logger
logger = get_logger(__name__)

def config_print_graph(graph, name: str):
    config = get_config()

    if config.graph.print:
        threading.Thread(target=lambda: asyncio.run(print(graph, name))).start()

async def print(graph, name: str):
    """Imprime o grafo em formato de imagem."""

    logger.info("Imprimindo grafo")

    png_bytes = graph.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.API
    )

    timestamp = int(datetime.now().timestamp())

    file_name = str(timestamp) + "_" + name + ".png"
    with open("temp/images/" + file_name, "wb") as f:
        f.write(png_bytes)

    logger.info("Grafo impresso")
