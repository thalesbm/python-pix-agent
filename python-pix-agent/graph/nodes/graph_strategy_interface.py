from abc import ABC, abstractmethod

from graph.graph_state import GraphState

class GraphStrategyInterface(ABC):
    
    @abstractmethod
    def build(self, state: GraphState) -> GraphState:
        pass
