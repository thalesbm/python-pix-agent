"""
Sistema de logging centralizado para o Doc Expert Agent.
Fornece configuração unificada e utilitários de logging.
"""

import logging
import os
from pathlib import Path


class LoggerConfig:
    """Configuração centralizada de logging."""
    
    # Configurações padrão
    DEFAULT_LEVEL = "INFO"
    DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
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
        log_file: str = None,
        console_output: bool = True,
        file_output: bool = True
    ):
        """
        Configura o sistema de logging.
        
        Args:
            level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            format_string: Formato das mensagens de log
            log_file: Nome do arquivo de log (opcional)
            console_output: Se deve exibir logs no console
            file_output: Se deve salvar logs em arquivo
        """
        if self._configured:
            return
        
        # Usa configurações padrão se não fornecidas
        level = level or self.DEFAULT_LEVEL
        format_string = format_string or self.DEFAULT_FORMAT
        
        # Cria o diretório de logs se não existir
        if file_output:
            Path(self.LOG_DIR).mkdir(exist_ok=True)
        
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
        
        # Handler para arquivo
        if file_output and log_file:
            file_path = os.path.join(self.LOG_DIR, log_file)
            file_handler = logging.FileHandler(file_path, encoding='utf-8')
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        self._configured = True
        
        # Log inicial
        logger = logging.getLogger(__name__)
        logger.info(f"Logging configurado - Nível: {level}, Console: {console_output}, Arquivo: {file_output}")
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        Obtém um logger configurado para o módulo especificado.
        
        Args:
            name: Nome do módulo (geralmente __name__)
            
        Returns:
            Logger configurado
        """
        if name in self._loggers:
            return self._loggers[name]
        
        logger = logging.getLogger(name)
        self._loggers[name] = logger
        return logger
    
    def set_level(self, level: str):
        """
        Define o nível de logging para todos os loggers.
        
        Args:
            level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        logging.getLogger().setLevel(getattr(logging, level.upper()))
        
        # Atualiza todos os loggers registrados
        for logger in self._loggers.values():
            logger.setLevel(getattr(logging, level.upper()))
    
    def add_file_handler(self, log_file: str, level: str = None):
        """
        Adiciona um handler de arquivo adicional.
        
        Args:
            log_file: Nome do arquivo de log
            level: Nível de logging para este handler
        """
        if not self._configured:
            raise RuntimeError("Logging deve ser configurado antes de adicionar handlers")
        
        # Cria o diretório se não existir
        Path(self.LOG_DIR).mkdir(exist_ok=True)
        
        # Configura o formato
        formatter = logging.Formatter(
            fmt=self.DEFAULT_FORMAT,
            datefmt=self.DEFAULT_DATE_FORMAT
        )
        
        # Cria o handler
        file_path = os.path.join(self.LOG_DIR, log_file)
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        if level:
            file_handler.setLevel(getattr(logging, level.upper()))
        
        # Adiciona ao logger raiz
        logging.getLogger().addHandler(file_handler)
        
        logger = logging.getLogger(__name__)
        logger.info(f"Handler de arquivo adicionado: {log_file}")


# Instância global do configurador de logging
logger_config = LoggerConfig()


def setup_logging(
    level: str = None,
    format_string: str = None,
    log_file: str = None,
    console_output: bool = True,
    file_output: bool = True
):
    """
    Função de conveniência para configurar logging.
    
    Args:
        level: Nível de logging
        format_string: Formato das mensagens
        log_file: Nome do arquivo de log
        console_output: Se deve exibir no console
        file_output: Se deve salvar em arquivo
    """
    logger_config.setup_logging(
        level=level,
        format_string=format_string,
        log_file=log_file,
        console_output=console_output,
        file_output=file_output
    )


def get_logger(name: str) -> logging.Logger:
    """
    Função de conveniência para obter um logger.
    
    Args:
        name: Nome do módulo
        
    Returns:
        Logger configurado
    """
    return logger_config.get_logger(name)


def set_log_level(level: str):
    """
    Função de conveniência para definir o nível de logging.
    
    Args:
        level: Nível de logging
    """
    logger_config.set_level(level)


def add_file_handler(log_file: str, level: str = None):
    """
    Função de conveniência para adicionar handler de arquivo.
    
    Args:
        log_file: Nome do arquivo
        level: Nível de logging
    """
    logger_config.add_file_handler(log_file, level)
