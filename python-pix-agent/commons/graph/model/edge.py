from dataclasses import dataclass

@dataclass(frozen=True)
class EdgeDef:
    src: str
    dst: str
