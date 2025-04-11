"""
Author: Mohamed Ibrahim Moselhy
Role: Senior RPA Developer
Description: 
    This script monitors a specified folder for new files using the watchdog library.
    When a new file is detected, its path is retrieved and returned for further processing.
    The script runs in an event-driven manner using threading.

Date: March 2025
"""

import os
import time
import threading
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set up logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler("logs/file_watcher.log", mode='a')
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class FileAddedHandler(FileSystemEventHandler):
    """Handles newly created files in the watched directory."""

    def __init__(self, event):
        """Initializes the event handler for file monitoring."""
        try:
            super().__init__()
            self.new_file_path = None
            self.event = event
            logger.info("Initialized FileAddedHandler.")
        except Exception as e:
            logger.exception("Error initializing FileAddedHandler.")
            raise RuntimeError(f"Error initializing FileAddedHandler: {e}") from e

    def on_created(self, event):
        """Handles newly created files in the watched directory."""
        try:
            if not event.is_directory:
                self.new_file_path = os.path.abspath(event.src_path)
                logger.info(f"New file detected: {self.new_file_path}")
                self.event.set()
        except Exception as e:
            logger.exception("Error processing file creation event.")
            raise RuntimeError(f"Error processing file creation event: {e}") from e

def monitor_folder(folder_to_watch):
    """Monitors a folder for new files and returns the detected file path."""
    try:
        logger.info(f"Starting folder monitor on: {folder_to_watch}")
        previous_files = get_all_files(folder_to_watch)
        
        while True:
            time.sleep(5)
            current_files = get_all_files(folder_to_watch)
            new_files = current_files - previous_files
            
            if new_files:
                for file in new_files:
                    logger.info(f"New file detected: {file}")
                    return file
            
            previous_files = current_files

    except KeyboardInterrupt:
        logger.info("File watcher stopped by user.")
        return None
    except Exception as e:
        logger.exception("Unexpected error in monitor_folder.")
        raise RuntimeError(f"Unexpected error in monitor_folder: {e}") from e

def get_all_files(folder_path):
    try:
        file_paths = set()
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_paths.add(os.path.join(root, file))
        return file_paths
    except Exception as e:
        logger.exception("Error while scanning files.")
        raise
