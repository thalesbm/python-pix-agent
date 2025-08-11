from graph.graph_state import GraphState
from graph.nodes.limits.verify_value import VerifyLimitValueNodeStrategy
from graph.nodes.limits.update_limit import UpdateLimitNodeStrategy
from graph.nodes.receipt.receipt import ReceiptNodeStrategy
from graph.nodes.llm.format_answer_from_state import FormatAnswerFromStateNodeStrategy
from graph.nodes.generic.clean_state import CleanStateNodeStrategy
from graph.nodes.generic.finish_simple_flow import FinishSimpleFlowNodeStrategy

from commons.graph.graph_interface import GraphFactory
from commons.graph.model.graph import GraphBlueprint    
from commons.graph.model.node import Node 
from commons.graph.model.edge import Edge
from commons.graph.model.router import Router
from commons.graph.graph_blueprint import GraphBlueprintBuilder 

from logger import get_logger
logger = get_logger(__name__)

class UpdateLimitGraphFactory(GraphFactory):
    
    def __init__(self):
        pass

    def build(self) -> GraphBlueprint:
        """
        Cria o workflow de atualizar limite do grafo.
        """
        logger.info("Criando UpdateLimitGraph")

        graph_blueprint = GraphBlueprint(
            id="update_limit",
            entry=VerifyLimitValueNodeStrategy.name(),
            nodes=[
                Node(VerifyLimitValueNodeStrategy.name(), VerifyLimitValueNodeStrategy),
                Node(UpdateLimitNodeStrategy.name(), UpdateLimitNodeStrategy),
                Node(ReceiptNodeStrategy.name(), ReceiptNodeStrategy),
                Node(FormatAnswerFromStateNodeStrategy.name(), FormatAnswerFromStateNodeStrategy),
                Node(FinishSimpleFlowNodeStrategy.name(), FinishSimpleFlowNodeStrategy),
                Node(CleanStateNodeStrategy.name(), CleanStateNodeStrategy),
            ],
            routers=[
                Router(
                    source=VerifyLimitValueNodeStrategy.name(),   
                    func=self.decidir_proximo_no_limit,
                    cases={
                        UpdateLimitNodeStrategy.name(): UpdateLimitNodeStrategy.name(),
                        FinishSimpleFlowNodeStrategy.name(): FinishSimpleFlowNodeStrategy.name(),
                    },
                ),
            ],
            edges=[
                Edge(UpdateLimitNodeStrategy.name(), ReceiptNodeStrategy.name()),
                Edge(ReceiptNodeStrategy.name(), FormatAnswerFromStateNodeStrategy.name()),
                Edge(FormatAnswerFromStateNodeStrategy.name(), CleanStateNodeStrategy.name()),
            ],
            end_nodes=[CleanStateNodeStrategy.name(), FinishSimpleFlowNodeStrategy.name()],
        )

        graph = GraphBlueprintBuilder(GraphState).build(graph_blueprint)
        
        logger.info("UpdateLimitGraph criado")

        return graph

    @staticmethod
    def decidir_proximo_no_limit(state: GraphState) -> str:
        if state.limit.has_limit:
            return UpdateLimitNodeStrategy.name()
        else:
            return FinishSimpleFlowNodeStrategy.name()
