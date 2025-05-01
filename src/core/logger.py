"""
Enhanced logging module with detailed logging capabilities
"""

import logging
import os
from datetime import datetime
from src.core.constants import *
import time
import sys
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self):
        self.setup_logger()

    def setup_logger(self):
        # Get the application directory
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            app_dir = os.path.dirname(sys.executable)
        else:
            # Running as script
            app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Create logs directory in application directory
        logs_dir = os.path.join(app_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)

        # Set up the logger
        self.logger = logging.getLogger("WhatsAppAutoSender")
        self.logger.setLevel(logging.DEBUG)

        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )

        # File handler with rotation
        log_file = os.path.join(logs_dir, f"whatsapp_auto_sender_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)

        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def exception(self, message):
        self.logger.exception(message)

    def log_performance(self, operation: str, start_time: float):
        """Log performance metrics for an operation"""
        duration = time.time() - start_time
        self.logger.info(f"Performance - {operation}: {duration:.2f} seconds")

# Create a global logger instance
logger = Logger() 