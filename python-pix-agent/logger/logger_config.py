"""
Sistema de logging centralizado para o Doc Expert Agent.
Fornece configuração unificada e utilitários de logging.
"""

import logging

class LoggerConfig:
    """Configuração centralizada de logging."""
    
    # Configurações padrão
    DEFAULT_LEVEL = "INFO"
    DEFAULT_FORMAT = "%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s: %(message)s"
    DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # Diretório de logs
    LOG_DIR = "logs"
    
    def __init__(self):
        self._configured = False
        self._loggers = {}
    
    def setup_logging(
        self,
        level: str = None,
        format_string: str = None,
        console_output: bool = True,
    ):
        if self._configured:
            return
        
        # Usa configurações padrão se não fornecidas
        level = level or self.DEFAULT_LEVEL
        format_string = format_string or self.DEFAULT_FORMAT
        
        # Configura o formato
        formatter = logging.Formatter(
            fmt=format_string,
            datefmt=self.DEFAULT_DATE_FORMAT
        )
        
        # Configura o logger raiz
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, level.upper()))
        
        # Remove handlers existentes para evitar duplicação
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Handler para console
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        self._configured = True
        
        # Log inicial
        logger = logging.getLogger(__name__)
        logger.info(f"Logging configurado - Nível: {level}, Console: {console_output}")
    
    def get_logger(self, name: str) -> logging.Logger:
        if name in self._loggers:
            return self._loggers[name]
        
        logger = logging.getLogger(name)
        self._loggers[name] = logger
        return logger
    
    def set_level(self, level: str):
        logging.getLogger().setLevel(getattr(logging, level.upper()))
        
        # Atualiza todos os loggers registrados
        for logger in self._loggers.values():
            logger.setLevel(getattr(logging, level.upper()))

# Instância global do configurador de logging
logger_config = LoggerConfig()

def setup_logging(
    level: str = None,
    format_string: str = None,
    console_output: bool = True,
):
    logger_config.setup_logging(
        level=level,
        format_string=format_string,
        console_output=console_output,
    )


def get_logger(name: str) -> logging.Logger:
    return logger_config.get_logger(name)


def set_log_level(level: str):
    logger_config.set_level(level)
