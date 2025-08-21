from graph.graphs.main_graph import MainGraph
from graph.graph_state import GraphState

from commons.logger import get_logger
logger = get_logger(__name__)

class MainController:
    def __init__(self):
        pass

    def run(self, message: str, user_id: str):
        """
        Executa o workflow principal.
        """
        logger.info(f"Mensagem recebida na MainController: {message}")

        return MainGraph().build(message=message, user_id=user_id)
