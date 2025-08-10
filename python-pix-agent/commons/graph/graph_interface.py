from abc import ABC, abstractmethod
from commons.graph.model.graph import GraphBlueprint

class GraphFactory(ABC):
    @abstractmethod
    def build(self) -> GraphBlueprint:
        pass
