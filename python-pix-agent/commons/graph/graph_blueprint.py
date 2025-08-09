from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from commons.graph.model.graph import GraphBlueprint

import asyncio
import threading
from utils.print_graph import print_graph

class GraphBlueprintBuilder:

    def __init__(self, state_type):
        self.state_type = state_type

    def build(self, graph_blueprint: GraphBlueprint):
        """
        Cria o grafo com base no blueprint.
        """
        graph_builder = StateGraph(self.state_type)
        
        self._add_nodes(graph_builder, graph_blueprint)
        self._add_edges(graph_builder, graph_blueprint)
        self._add_endpoints(graph_builder, graph_blueprint)
        self._after_build(graph_builder, graph_blueprint)
        
        return graph_builder.compile()

    def _add_nodes(self, graph_builder: StateGraph, graph_blueprint: GraphBlueprint):
        """
        Adiciona os nós ao grafo.
        """
        for n in graph_blueprint.nodes:
            graph_builder.add_node(n.name, self._wrap(n.strategy_factory))

        if graph_blueprint.routers:
            for r in graph_blueprint.routers:
                graph_builder.add_node(r.name, RunnableLambda(lambda st, f=r.func: {"next": f(st)}))

    def _wrap(self, strategy_factory):
        """
        Padroniza o wrapping + decorators, retries, trace, etc.
        """
        return RunnableLambda(strategy_factory().build)

    def _add_edges(self, graph_builder: StateGraph, graph_blueprint: GraphBlueprint):
        """
        Adiciona as arestas ao grafo.
        """
        for e in graph_blueprint.edges:
            graph_builder.add_edge(e.src, e.dst)

        graph_builder.set_entry_point(graph_blueprint.entry)

    def _add_endpoints(self, graph_builder: StateGraph, graph_blueprint: GraphBlueprint):
        """
        Adiciona os pontos finais ao grafo.
        """
        ends = set((graph_blueprint.end_nodes or []))

        for e in ends:
            graph_builder.add_edge(e, END)

    def _after_build(self, graph_builder, graph_blueprint):
        """
        Imprime o grafo após a construção.
        """
        threading.Thread(target=lambda: asyncio.run(self.print(graph_builder, graph_blueprint))).start()

    async def print(self, graph_builder, graph_blueprint):
        print_graph(graph_builder, graph_blueprint.id)
