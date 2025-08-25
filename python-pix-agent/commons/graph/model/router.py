from dataclasses import dataclass, field
from typing import Callable, Dict, List 
from graph.state.graph_state import GraphState


@dataclass(frozen=True)
class Router:
    func: Callable[[GraphState], str]
    cases: Dict[str, str] = field(default_factory=dict)
    dst: List[str] = field(default_factory=list)  
    source: str = ""

    def get_cases(self) -> Dict[str, str]:
        if self.cases:
            return self.cases
        return {d: d for d in self.dst}
