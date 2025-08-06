from graph.graphs.main_graph import MainGraph

from logger import get_logger
logger = get_logger(__name__)

class MainController:
    def __init__(self):
        pass

    def run(self, message: str):
        logger.info(f"Mensagem recebida na MainController: {message}")

        return MainGraph().build(message)
