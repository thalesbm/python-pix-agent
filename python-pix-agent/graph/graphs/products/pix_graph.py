from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from graph.graph_state import GraphState
from graph.nodes.pix.check_value_key import CheckValueKeyNodeStrategy
from graph.nodes.pix.simulate_pix import SimulatePixNodeStrategy
from graph.nodes.pix.effective_pix import EffectivePixNodeStrategy
from graph.nodes.pix.get_contact_pix import GetContactPixNodeStrategy
from graph.nodes.pix.verify_date_pix import VerifyDatePixNodeStrategy
from graph.nodes.limits.get_limit import GetLimitNodeStrategy
from graph.nodes.balance.get_balance import GetBalanceNodeStrategy
from graph.nodes.receipt.receipt import ReceiptNodeStrategy
from graph.nodes.generic.finish_simple_flow import FinishSimpleFlowNodeStrategy
from graph.nodes.llm.format_answer_from_state import FormatAnswerFromStateNodeStrategy
from graph.nodes.generic.clean_state import CleanStateNodeStrategy

from commons.utils.print_graph import config_print_graph

from commons.logger import get_logger
logger = get_logger(__name__)

class PixGraph:
    def __init__(self):
        pass

    @staticmethod
    def name() -> str:
        return "pix-graph"

    def build(self, state: GraphState) -> GraphState:
        """
        Cria o workflow de pix do grafo.
        """
        logger.info("Criando PixGraph")

        graph_builder = StateGraph(GraphState)

        graph_builder.add_node(CheckValueKeyNodeStrategy.name(), RunnableLambda(CheckValueKeyNodeStrategy().build))
        graph_builder.add_node(SimulatePixNodeStrategy.name(), RunnableLambda(SimulatePixNodeStrategy().build))
        graph_builder.add_node(EffectivePixNodeStrategy.name(), RunnableLambda(EffectivePixNodeStrategy().build))
        graph_builder.add_node(GetContactPixNodeStrategy.name(), RunnableLambda(GetContactPixNodeStrategy().build))
        graph_builder.add_node(VerifyDatePixNodeStrategy.name(), RunnableLambda(VerifyDatePixNodeStrategy().build))
        graph_builder.add_node(GetLimitNodeStrategy.name(), RunnableLambda(GetLimitNodeStrategy().build))
        graph_builder.add_node(GetBalanceNodeStrategy.name(), RunnableLambda(GetBalanceNodeStrategy().build))
        graph_builder.add_node(ReceiptNodeStrategy.name(), RunnableLambda(ReceiptNodeStrategy().build))
        graph_builder.add_node(FinishSimpleFlowNodeStrategy.name(), RunnableLambda(FinishSimpleFlowNodeStrategy().build))
        graph_builder.add_node(FormatAnswerFromStateNodeStrategy.name(), RunnableLambda(FormatAnswerFromStateNodeStrategy().build))
        graph_builder.add_node(CleanStateNodeStrategy.name(), RunnableLambda(CleanStateNodeStrategy().build))

        graph_builder.set_entry_point(CheckValueKeyNodeStrategy.name())

        graph_builder.add_conditional_edges(
            CheckValueKeyNodeStrategy.name(),
            self.decidir_proximo_no_depois_input,
            {
                GetBalanceNodeStrategy.name(): GetBalanceNodeStrategy.name(),
                FinishSimpleFlowNodeStrategy.name(): FinishSimpleFlowNodeStrategy.name(),
            }
        )

        # Pix
        graph_builder.add_edge(VerifyDatePixNodeStrategy.name(), GetBalanceNodeStrategy.name())
        graph_builder.add_edge(GetBalanceNodeStrategy.name(), GetLimitNodeStrategy.name())
        graph_builder.add_edge(GetLimitNodeStrategy.name(), GetContactPixNodeStrategy.name())
        graph_builder.add_edge(GetContactPixNodeStrategy.name(), SimulatePixNodeStrategy.name())
        graph_builder.add_edge(SimulatePixNodeStrategy.name(), EffectivePixNodeStrategy.name())
        graph_builder.add_edge(EffectivePixNodeStrategy.name(), ReceiptNodeStrategy.name())
        graph_builder.add_edge(ReceiptNodeStrategy.name(), FormatAnswerFromStateNodeStrategy.name())
        graph_builder.add_edge(FormatAnswerFromStateNodeStrategy.name(), CleanStateNodeStrategy.name())
        graph_builder.add_edge(CleanStateNodeStrategy.name(), END)
        graph_builder.add_edge(FinishSimpleFlowNodeStrategy.name(), END)

        graph = graph_builder.compile().invoke(state)

        config_print_graph(graph, "pix")

        logger.info("PixGraph criado")

        return state

    @staticmethod
    def decidir_proximo_no_depois_input(state: GraphState) -> str:
        logger.info("================================================")
        logger.info(f"Value: {state.pix.has_value}")
        logger.info(f"Key: {state.pix.has_key}")
        logger.info("================================================")

        if state.pix.has_value and state.pix.has_key:
            return GetBalanceNodeStrategy.name()
        else:
            return FinishSimpleFlowNodeStrategy.name()
