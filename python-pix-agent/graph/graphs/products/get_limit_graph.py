from graph.graph_state import GraphState
from graph.nodes.limits.get_limit import GetLimitNodeStrategy
from graph.nodes.llm.format_answer_from_state import FormatAnswerFromStateNodeStrategy
from graph.nodes.generic.clean_state import CleanStateNodeStrategy

from commons.graph.graph_interface import GraphFactory
from commons.graph.model.graph import GraphBlueprint
from commons.graph.model.node import Node
from commons.graph.model.edge import Edge
from commons.graph.graph_blueprint import GraphBlueprintBuilder

from commons.logger import get_logger
logger = get_logger(__name__)

class GetLimitGraphFactory(GraphFactory):

    @staticmethod
    def name() -> str:
        return "get-limit-graph"

    def build(self, state: GraphState) -> GraphState:    
        """
        Cria o workflow de limite do grafo.
        """
        logger.info("Criando GetLimitGraph")

        graph = GraphBlueprint(
            id="get_limit",
            entry=GetLimitNodeStrategy.name(),
            nodes=[
                Node(GetLimitNodeStrategy.name(), GetLimitNodeStrategy),
                Node(FormatAnswerFromStateNodeStrategy.name(), FormatAnswerFromStateNodeStrategy),
                Node(CleanStateNodeStrategy.name(), CleanStateNodeStrategy),
            ],
            edges=[
                Edge(GetLimitNodeStrategy.name(), FormatAnswerFromStateNodeStrategy.name()),
                Edge(FormatAnswerFromStateNodeStrategy.name(), CleanStateNodeStrategy.name()),
            ],
            end_nodes=[CleanStateNodeStrategy.name()],
        )

        GraphBlueprintBuilder(GraphState).build(graph, state)

        logger.info("GetLimitGraph criado")

        return state
