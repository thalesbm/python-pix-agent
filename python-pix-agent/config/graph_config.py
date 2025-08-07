from dataclasses import dataclass

@dataclass
class GraphConfig:
    """Configurações de logging."""
    print: bool = True