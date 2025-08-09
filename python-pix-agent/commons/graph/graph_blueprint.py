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
        self._after_build(graph_builder)
        
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
        return RunnableLambda(strategy_factory)

    def _add_edges(self, g, bp):
        """
        Adiciona as arestas ao grafo.
        """
        for e in bp.edges:
            g.add_edge(e.src, e.dst)
        g.set_entry_point(bp.entry)

    def _add_endpoints(self, g, bp):
        """
        Adiciona os pontos finais ao grafo.
        """
        ends = set((bp.end_nodes or []))
        for e in ends:
            g.add_edge(e, END)

    def _after_build(self, graph_builder):
        """
        Imprime o grafo após a construção.
        """
        threading.Thread(target=lambda: asyncio.run(print_graph(graph_builder))).start()
