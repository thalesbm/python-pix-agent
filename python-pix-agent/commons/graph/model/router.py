from dataclasses import dataclass
from typing import Callable
from graph.graph_state import GraphState

@dataclass(frozen=True)
class RouterDef:
    name: str
    func: Callable[[GraphState], str]
