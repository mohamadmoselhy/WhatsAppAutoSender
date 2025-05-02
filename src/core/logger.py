"""
Enhanced logging module with detailed logging capabilities
"""

import logging
import os
from datetime import datetime
from src.core.constants import *
import time

class Logger:
    def __init__(self):
        self.logger = logging.getLogger("WhatsAppAutoSender")
        self.setup_logger()

    def setup_logger(self):
        """Configure the logger with file and console handlers"""
        try:
            # Create logs directory if it doesn't exist
            os.makedirs("logs", exist_ok=True)
            
            # Set log level
            self.logger.setLevel(LOG_LEVEL)
            
            # Create formatters
            formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
            
            # File handler
            log_file = os.path.join("logs", f"{datetime.now().strftime('%Y%m%d')}_{LOG_FILE}")
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            
            # Add handlers
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
            
            self.log_info("Logger initialized successfully")
            
        except Exception as e:
            print(f"Failed to initialize logger: {str(e)}")
            raise

    def log_info(self, message: str):
        """Log an info message"""
        self.logger.info(message)

    def log_error(self, exception: Exception, message: str):
        """Log an error message with optional exception"""
        if exception:
            self.logger.error(f"{message} - Exception: {str(exception)}", exc_info=True)
        else:
            self.logger.error(message)

    def log_warning(self, message: str):
        """Log a warning message"""
        self.logger.warning(message)

    def log_debug(self, message: str):
        """Log a debug message"""
        self.logger.debug(message)

    def log_critical(self, message: str):
        """Log a critical message"""
        self.logger.critical(message)

    def log_exception(self, exception: Exception, message: str):
        """Log an exception with full traceback"""
        self.logger.exception(f"{message} - Exception: {str(exception)}")

    def log_performance(self, operation: str, start_time: float):
        """Log performance metrics for an operation"""
        duration = time.time() - start_time
        self.logger.info(f"Performance - {operation}: {duration:.2f} seconds")

# Create global logger instance
logger = Logger() 