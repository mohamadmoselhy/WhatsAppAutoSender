"""
Logging configuration for WhatsApp Auto Sender
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Optional
from pathlib import Path

class Logger:
    def __init__(self, name: str = "app_log", log_dir: str = "logs"):
        self.name = name
        self.log_dir = log_dir
        self.logger = logging.getLogger(name)
        self.setup_logger()

    def setup_logger(self) -> None:
        """Setup the logger with file and console handlers"""
        # Create log directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Clear existing handlers
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        
        # Set log level
        self.logger.setLevel(logging.INFO)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # File handler with rotation
        log_file = os.path.join(
            self.log_dir, 
            f"{self.name}_{datetime.now().strftime('%Y-%m-%d')}.log"
        )
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_error(self, error: Exception, context: Optional[str] = None) -> None:
        """Log an error with context"""
        error_msg = f"Error: {str(error)}"
        if context:
            error_msg = f"{context} - {error_msg}"
        self.logger.error(error_msg, exc_info=True)

    def log_info(self, message: str) -> None:
        """Log an info message"""
        self.logger.info(message)

    def log_warning(self, message: str) -> None:
        """Log a warning message"""
        self.logger.warning(message)

    def log_debug(self, message: str) -> None:
        """Log a debug message"""
        self.logger.debug(message)

# Create global logger instance
logger = Logger() 