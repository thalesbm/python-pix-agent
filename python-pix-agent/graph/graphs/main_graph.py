from graph.graph_state import GraphState
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda, RunnableBranch
from graph.nodes.llm.check_intention import check_intention
from graph.graphs.products import BalanceGraph, GetLimitGraph, UpdateLimitGraph, PixGraph
from graph.graphs import FallbackGraph

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.graph_state import GraphState
from graph.nodes.fallback.fallback import fallback
from utils.print_graph import print_graph

from logger import get_logger
logger = get_logger(__name__)

class MainGraph:
    def __init__(self):
        pass

    def build(self, message: str):    
        logger.info("Criando MainGraph")
        
        graph_builder = StateGraph(GraphState)

        router = self.build_router()
        
        graph_builder.add_node("verificar_intencao", RunnableLambda(check_intention))
        graph_builder.add_node("router", router)

        graph_builder.set_entry_point("verificar_intencao")

        graph_builder.add_edge("verificar_intencao", "router")

        raw_state = graph_builder.compile().invoke(GraphState(user_message=message))
        
        final_state = GraphState(**raw_state) 

        print(f"Saldo retornado pelo grafo: {final_state.balance.value}")

    def build_router(self):
        """
            O router é responsável por direcionar o fluxo do grafo com base na intenção do usuário.
        """
        saldo_graph = BalanceGraph().build()
        get_limite_graph = GetLimitGraph().build()
        update_limit_graph = UpdateLimitGraph().build()
        pix_graph = PixGraph().build()
        fallback_graph = FallbackGraph().build()

        router = RunnableBranch(
            (lambda state: state.intention == "consultar_limite", get_limite_graph),
            (lambda state: state.intention == "alterar_limite", update_limit_graph),
            (lambda state: state.intention == "consultar_saldo", saldo_graph),
            (lambda state: state.intention == "realizar_pix", pix_graph),
            fallback_graph
        )

        return router

    async def print(self, graph):
        print_graph(graph, "main")
