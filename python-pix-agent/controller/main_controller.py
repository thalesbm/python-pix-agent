from graph.graph_state import GraphState
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda, RunnableBranch
from graph.nodes.check_intention import check_intention
from graph.graphs import BalanceGraph, GetLimitGraph, UpdateLimitGraph, PixGraph, FallbackGraph

from logger import get_logger
logger = get_logger(__name__)

class MainController:
    def __init__(self):
        pass

    def run(self, message: str):
        logger.info(f"Mensagem recebida na MainController: {message}")

        saldo_graph = BalanceGraph().build()
        get_limite_graph = GetLimitGraph().build()
        update_limit_graph = UpdateLimitGraph().build()
        pix_graph = PixGraph().build()
        fallback_graph = FallbackGraph().build()

        router = RunnableBranch(
            (lambda state: state.intention == "consultar_limite", get_limite_graph),
            (lambda state: state.intention == "alterar_limite", update_limit_graph),
            (lambda state: state.intention == "saldo", saldo_graph),
            (lambda state: state.intention == "pix", pix_graph),
            fallback_graph
        )
    
        graph_builder = StateGraph(GraphState)
        graph_builder.add_node("verificar_intencao", RunnableLambda(check_intention))
        graph_builder.add_node("router", router)

        graph_builder.set_entry_point("verificar_intencao")

        graph_builder.add_edge("verificar_intencao", "router")

        main_graph = graph_builder.compile()
        main_graph.invoke(GraphState(user_message=message))
