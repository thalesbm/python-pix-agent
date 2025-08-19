from commons.graph.model.graph import GraphBlueprint
from commons.graph.model.node import Node
from commons.graph.model.edge import Edge
from commons.graph.graph_blueprint import GraphBlueprintBuilder
from graph.graph_state import GraphState
from graph.nodes.balance.get_balance import GetBalanceNodeStrategy
from graph.nodes.llm.format_answer_from_state import FormatAnswerFromStateNodeStrategy
from graph.nodes.generic.clean_state import CleanStateNodeStrategy
from commons.graph.graph_interface import GraphFactory

from commons.logger import get_logger
logger = get_logger(__name__)

class BalanceGraphFactory(GraphFactory):
    
    def build(self) -> GraphBlueprint:
        """
        Cria o workflow de saldo do grafo.
        """

        logger.info("Criando BalanceGraph")

        graph_blueprint = GraphBlueprint(
            id="balance",
            entry=GetBalanceNodeStrategy.name(),
            nodes=[
                Node(GetBalanceNodeStrategy.name(), GetBalanceNodeStrategy),
                Node(FormatAnswerFromStateNodeStrategy.name(), FormatAnswerFromStateNodeStrategy),
                Node(CleanStateNodeStrategy.name(), CleanStateNodeStrategy),
            ],
            edges=[
                Edge(GetBalanceNodeStrategy.name(), FormatAnswerFromStateNodeStrategy.name()),
                Edge(FormatAnswerFromStateNodeStrategy.name(), CleanStateNodeStrategy.name()),
            ],
            end_nodes=[CleanStateNodeStrategy.name()],
        )

        graph = GraphBlueprintBuilder(GraphState).build(graph_blueprint)
        
        return graph
