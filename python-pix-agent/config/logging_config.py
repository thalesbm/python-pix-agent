from dataclasses import dataclass
import os

@dataclass
class LoggingConfig:
    """Configurações de logging."""
    level: str = "DEBUG"
    format: str = "%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s: %(message)s"
    file_path: str = os.getenv("LOG_FILE", "app.log")