from dataclasses import dataclass
from typing import List
from commons.graph.model.node import NodeDef
from commons.graph.model.edge import EdgeDef
from commons.graph.model.router import RouterDef

@dataclass(frozen=True)
class GraphBlueprint:
    id: str
    entry: str
    nodes: List[NodeDef]
    edges: List[EdgeDef]
    routers: List[RouterDef] = None
    end_nodes: List[str] = None