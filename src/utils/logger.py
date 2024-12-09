import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

class Logger:
    """Centralized logging configuration for VocabMaster"""
    
    _instance: Optional['Logger'] = None
    
    def __init__(self, log_file: str):
        if Logger._instance is not None:
            raise RuntimeError("Logger is a singleton. Use Logger.get_instance() instead.")
            
        self.logger = logging.getLogger('VocabMaster')
        self.logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create rotating file handler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=1024 * 1024,  # 1MB
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        Logger._instance = self

    @classmethod
    def get_instance(cls, log_file: Optional[str] = None) -> 'Logger':
        """Get or create Logger instance"""
        if cls._instance is None:
            if log_file is None:
                raise ValueError("log_file is required when creating new Logger instance")
            cls(log_file)
        return cls._instance

    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)

    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)

    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)

    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)

    def exception(self, message: str):
        """Log exception with traceback"""
        self.logger.exception(message)
