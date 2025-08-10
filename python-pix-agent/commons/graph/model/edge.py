from dataclasses import dataclass

@dataclass(frozen=True)
class Edge:
    src: str
    dst: str
