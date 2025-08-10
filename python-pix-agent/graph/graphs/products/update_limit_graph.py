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
            entry="verificar_valor",
            nodes=[
                Node("verificar_valor", VerifyLimitValueNodeStrategy),
                Node("atualizar_limite", UpdateLimitNodeStrategy),
                Node("comprovante", ReceiptNodeStrategy),
                Node("formatar_resposta", FormatAnswerFromStateNodeStrategy),
                Node("encerrar_fluxo_simples", FinishSimpleFlowNodeStrategy),
                Node("limpar_estado", CleanStateNodeStrategy),
            ],
            routers=[
                Router(
                    source="verificar_valor",
                    func=self.decidir_proximo_no_limit,
                    cases={
                        "atualizar_limite": "atualizar_limite",
                        "encerrar_fluxo_simples": "encerrar_fluxo_simples",
                    },
                ),
            ],
            edges=[
                Edge("atualizar_limite", "comprovante"),
                Edge("comprovante", "formatar_resposta"),
                Edge("formatar_resposta", "limpar_estado"),
            ],
            end_nodes=["limpar_estado", "encerrar_fluxo_simples"],
        )

        graph = GraphBlueprintBuilder(GraphState).build(graph_blueprint)
        
        logger.info("UpdateLimitGraph criado")

        return graph

    @staticmethod
    def decidir_proximo_no_limit(state: GraphState) -> str:
        if state.limit.has_limit:
            return "atualizar_limite"
        else:
            return "encerrar_fluxo_simples"
