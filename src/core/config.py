"""
Configuration module for WhatsApp Auto Sender
"""

import os
import sys
from pathlib import Path
from src.core.constants import *
from src.core.logger import logger

class Config:
    def __init__(self):
        self._setup_paths()
        self._setup_logging()
        self._setup_file_watching()
        self._setup_message_template()
        self._validate_config()

    def _setup_paths(self):
        """Setup file system paths"""
        try:
            # Determine if we're running as an executable
            if getattr(sys, 'frozen', False):
                # Running as executable
                self.base_dir = Path(sys._MEIPASS)
            else:
                # Running as script
                self.base_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

            # Base paths
            self.folder_to_watch = DEFAULT_FOLDER_TO_WATCH
            self.TempMessageForGroupPath = os.path.join(self.base_dir, DEFAULT_TEMP_MESSAGE_PATH)
            self.root_path = DEFAULT_ROOT_PATH

            # Create necessary directories
            os.makedirs(self.folder_to_watch, exist_ok=True)
            logger.log_info(f"Created/verified folder to watch: {self.folder_to_watch}")

        except Exception as e:
            logger.log_error(e, "Failed to setup paths")
            raise

    def _setup_logging(self):
        """Setup logging configuration"""
        try:
            self.log_level = LOG_LEVEL
            self.log_format = LOG_FORMAT
            self.log_date_format = LOG_DATE_FORMAT
            logger.log_info("Logging configuration loaded")
        except Exception as e:
            logger.log_error(e, "Failed to setup logging")
            raise

    def _setup_file_watching(self):
        """Setup file watching configuration"""
        try:
            self.file_check_interval = FILE_CHECK_INTERVAL
            self.max_file_age = MAX_FILE_AGE
            self.file_patterns = FILE_PATTERNS
            logger.log_info("File watching configuration loaded")
        except Exception as e:
            logger.log_error(e, "Failed to setup file watching")
            raise

    def _setup_message_template(self):
        """Setup message template configuration"""
        try:
            self.message_placeholders = MESSAGE_PLACEHOLDERS
            self.message = os.path.exists(self.TempMessageForGroupPath)
            if self.message:
                logger.log_info(f"Message template found at: {self.TempMessageForGroupPath}")
            else:
                logger.log_warning(f"No message template found at: {self.TempMessageForGroupPath}")
        except Exception as e:
            logger.log_error(e, "Failed to setup message template")
            raise

    def _validate_config(self):
        """Validate the configuration"""
        try:
            # Validate paths
            if not os.path.exists(self.folder_to_watch):
                raise FileNotFoundError(f"Folder to watch does not exist: {self.folder_to_watch}")

            # Validate message template if enabled
            if self.message and not os.path.exists(self.TempMessageForGroupPath):
                raise FileNotFoundError(f"Message template not found: {self.TempMessageForGroupPath}")

            logger.log_info("Configuration validated successfully")
        except Exception as e:
            logger.log_error(e, "Configuration validation failed")
            raise

# Create global config instance
config = Config()
