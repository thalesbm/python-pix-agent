from commons.graph.model.graph import GraphBlueprint
from commons.graph.model.node import NodeDef
from commons.graph.model.edge import EdgeDef
from commons.graph.graph_blueprint import GraphBlueprintBuilder
from graph.graph_state import GraphState
from graph.nodes.balance.get_balance import GetBalanceNodeStrategy
from graph.nodes.llm.format_answer_from_state import FormatAnswerFromStateNodeStrategy
from graph.nodes.generic.clean_state import CleanStateNodeStrategy
from commons.graph.graph_interface import GraphFactory

from logger import get_logger
logger = get_logger(__name__)

class BalanceGraphFactory(GraphFactory):
    
    def build(self) -> GraphBlueprint:
        """
        Cria o workflow de saldo do grafo.
        """

        logger.info("Criando BalanceGraph")

        graph_blueprint = GraphBlueprint(
            id="balance",
            entry="saldo",
            nodes=[
                NodeDef("saldo", GetBalanceNodeStrategy),
                NodeDef("formatar_resposta", FormatAnswerFromStateNodeStrategy),
                NodeDef("limpar_estado", CleanStateNodeStrategy),
            ],
            edges=[
                EdgeDef("saldo", "formatar_resposta"),
                EdgeDef("formatar_resposta", "limpar_estado"),
            ],
            end_nodes=["limpar_estado"],
        )

        graph = GraphBlueprintBuilder(GraphState).build(graph_blueprint)
        
        return graph
