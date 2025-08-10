from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Node:
    name: str
    strategy_factory: Callable[[], object]
    