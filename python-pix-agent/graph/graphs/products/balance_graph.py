

from graph.nodes.balance.get_balance import GetBalanceNodeStrategy
from graph.nodes.llm.format_answer_from_state import FormatAnswerFromStateNodeStrategy
from graph.nodes.generic.clean_state import CleanStateNodeStrategy

from utils.print_graph import print_graph

from logger import get_logger
logger = get_logger(__name__)

from abc import ABC, abstractmethod
from commons.graph.model.graph import GraphBlueprint
from commons.graph.model.node import NodeDef
from commons.graph.model.edge import EdgeDef
from commons.graph.graph_blueprint import GraphBlueprintBuilder
from langgraph.graph import StateGraph
from graph.graph_state import GraphState

class GraphFactory(ABC):
    @abstractmethod
    def build(self) -> GraphBlueprint:
        pass

class BalanceGraphFactory(GraphFactory):
    
    def build(self) -> GraphBlueprint:
        """
        Cria o workflow de saldo do grafo.
        """

        logger.info("Criando BalanceGraph")

        graph_builder = GraphBlueprint(
            entry="saldo",
            nodes=[
                NodeDef("saldo", GetBalanceNodeStrategy().build()),
                NodeDef("formatar_resposta", FormatAnswerFromStateNodeStrategy().build()),
                NodeDef("limpar_estado", CleanStateNodeStrategy().build()),
            ],
            edges=[
                EdgeDef("saldo", "formatar_resposta"),
                EdgeDef("formatar_resposta", "limpar_estado"),
            ],
            end_nodes=["limpar_estado"],
        )

        graph = GraphBlueprintBuilder(GraphState).build(graph_builder)
        
        return graph

# class BalanceGraph:
#     def __init__(self):
#         pass

#     def build(self):
       
#         logger.info("Criando BalanceGraph")
        
#         graph_builder = StateGraph(GraphState)

#         graph_builder.add_node("saldo", RunnableLambda(GetBalanceNodeStrategy().build))
#         graph_builder.add_node("formatar_resposta", RunnableLambda(FormatAnswerFromStateNodeStrategy().build))
#         graph_builder.add_node("limpar_estado", RunnableLambda(CleanStateNodeStrategy().build))
        
#         graph_builder.set_entry_point("saldo")
        
#         graph_builder.add_edge("saldo", "formatar_resposta")
#         graph_builder.add_edge("formatar_resposta", "limpar_estado")
#         graph_builder.add_edge("limpar_estado", END)

#         graph = graph_builder.compile()
#         logger.info("BalanceGraph criado")

#         threading.Thread(target=lambda: asyncio.run(self.print(graph))).start()

#         return graph

    async def print(self, graph):
        print_graph(graph, "balance")
