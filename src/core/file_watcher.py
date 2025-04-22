"""
File watching functionality for WhatsApp Auto Sender
"""

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Callable

from src.core.config import config
from src.core.logger import logger

class FileHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback

    def on_created(self, event):
        """Handle file creation events"""
        if not event.is_directory:
            file_path = event.src_path
            logger.log_info(f"File created: {file_path}")
            self.callback(file_path)

class FileWatcher:
    def __init__(self, folder_path: str, callback: Callable[[str], None]):
        self.folder_path = folder_path
        self.callback = callback
        self.observer = None

    def start(self) -> None:
        """Start watching the folder"""
        try:
            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path, exist_ok=True)
                logger.log_info(f"Created folder: {self.folder_path}")

            handler = FileHandler(self.callback)
            self.observer = Observer()
            self.observer.schedule(handler, self.folder_path, recursive=False)
            self.observer.start()
            logger.log_info(f"Started watching folder: {self.folder_path}")
        except Exception as e:
            logger.log_error(e, f"Error starting file watcher")
            raise

    def stop(self) -> None:
        """Stop watching the folder"""
        try:
            if self.observer:
                self.observer.stop()
                self.observer.join()
                self.observer = None
                logger.log_info(f"Stopped watching folder: {self.folder_path}")
        except Exception as e:
            logger.log_error(e, f"Error stopping file watcher")
            raise

# Create global watcher instance
watcher = FileWatcher(config.folder_to_watch, lambda x: None) 