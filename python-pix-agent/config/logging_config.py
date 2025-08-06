from dataclasses import dataclass

@dataclass
class LoggingConfig:
    """Configurações de logging."""
    level: str = "DEBUG"
    format: str = "%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s: %(message)s"