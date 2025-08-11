from dataclasses import dataclass
from typing import List
from commons.graph.model.node import Node
from commons.graph.model.edge import Edge
from commons.graph.model.router import Router

@dataclass(frozen=True)
class GraphBlueprint:
    id: str
    entry: str
    nodes: List[Node]
    edges: List[Edge]
    routers: List[Router] = None
    end_nodes: List[str] = None