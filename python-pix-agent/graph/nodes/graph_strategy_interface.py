from abc import ABC, abstractmethod

from graph.graph_state import GraphState

class GraphStrategyInterface(ABC):
    
    @abstractmethod
    def build(self, state: GraphState) -> GraphState:
        self.trace(state)

    def trace(self, state: GraphState):
        state.trace.append(self.__class__.__name__)
