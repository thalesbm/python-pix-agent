from dataclasses import dataclass
from typing import Callable, Dict
from graph.graph_state import GraphState

@dataclass(frozen=True)
class Router:
    func: Callable[[GraphState], str]
    cases: Dict[str, str]
    source: str  
