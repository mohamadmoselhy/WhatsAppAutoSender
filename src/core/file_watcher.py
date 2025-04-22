"""
File watching functionality for WhatsApp Auto Sender
"""

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
from typing import Callable
import re
import time

from src.core.config import config
from src.core.logger import logger


class DetailedFileHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self.processed_files = set()
        self.processing_files = set()

    def is_temporary_file(self, file_path: str) -> bool:
        """Check if the file is a temporary file"""
        if not file_path:  # Handle potential None or empty paths
            return False
        file_name = os.path.basename(file_path)
        if not file_name:  # Handle cases where path might end in a separator
            return False

        # Expanded temporary file patterns
        temp_patterns = [
            r'^~.*',                     # Starts with ~ (common for Office temp files)
            r'^~\$.*',                   # Excel temporary files
            r'^\.~.*',                   # Some editors create .~ prefixed files
            r'.*\.tmp$',                 # Ends with .tmp
            r'.*\.TMP$',                 # Ends with .TMP
            r'.*\.temp$',                # Some editors use .temp extension
            r'.*\.part$',                # Chrome/Firefox partial download
            r'.*\.crdownload$',          # Chrome download temp
            r'.*\.swp$',                 # Vim swap
            r'.*\.bak$',                 # Backup files
            r'.*~RF.*\.TMP$',            # Excel AutoRecovery
        ]

        is_temp = False
        for pattern in temp_patterns:
            if re.match(pattern, file_name, re.IGNORECASE):
                is_temp = True
                break

        logger.log_info(f"is_temporary_file check for '{file_name}': {is_temp}")
        return is_temp

    def is_stable_file(self, file_path: str) -> bool:
        """Check if the file size remains stable (i.e., it's not being written to)"""
        try:
            initial_size = os.path.getsize(file_path)
            time.sleep(1.5)  # Slightly longer wait for stability
            if not os.path.exists(file_path):
                return False
            final_size = os.path.getsize(file_path)
            return initial_size == final_size
        except Exception as e:
            logger.log_error(e, f"Failed to check file stability for: {file_path}")
            return False

    def process_event(self, event):
        """Unified event processing logic"""
        if event.is_directory:
            logger.log_info(f"Ignoring directory event: {event.src_path}")
            return

        file_path = event.src_path
        file_name = os.path.basename(file_path)
        event_type = event.event_type
        logger.log_info(f"Event received: type={event_type}, path={file_path}")

        # Skip if file is already being processed
        if file_path in self.processing_files:
            logger.log_info(f"Skipping event for already processing file: {file_name}")
            return

        # Skip if file has already been processed successfully
        if file_path in self.processed_files:
            logger.log_info(f"Skipping event for already processed file: {file_name}")
            return

        # Check if it's a temporary file
        if self.is_temporary_file(file_path):
            logger.log_info(f"Skipping temporary file based on check: {file_name}")
            return

        # --- Add a check for file stability ---
        if not self.is_stable_file(file_path):
            logger.log_info(f"File not stable yet: {file_name}")
            return

        # --- Process the file ---
        try:
            # Mark file as being processed
            self.processing_files.add(file_path)
            logger.log_info(f"Callback INVOKED for: {file_name} (Event: {event_type})")
            self.callback(file_path)

            # Mark file as processed *only after successful callback*
            self.processed_files.add(file_path)
            logger.log_info(f"Successfully processed: {file_name}")

        except Exception as e:
            logger.log_error(e, f"Error during callback execution for {file_name}")
            # Decide if you want to add to processed_files even on error,
            # maybe based on error type, to prevent retries.
            # For now, we don't add it on error.

        finally:
            # Always remove from processing set when done or on error
            self.processing_files.discard(file_path)
            logger.log_info(f"Finished processing attempt for: {file_name}")

    def on_created(self, event):
        self.process_event(event)

    def on_modified(self, event):
        """Triggered for file modifications."""
        logger.log_info(f"On_modified event triggered for {event.src_path}")
        self.process_event(event)

    # Optional: Handle moved files if necessary
    # def on_moved(self, event):
    #     logger.log_info(f"On_moved event from {event.src_path} to {event.dest_path}")
    #     pass


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

            # Use the detailed handler
            event_handler = DetailedFileHandler(self.callback)

            # Optional: Add watchdog's built-in logging handler for extra debug info
            # logging_handler = LoggingEventHandler()

            self.observer = Observer()
            self.observer.schedule(event_handler, self.folder_path, recursive=False)
            # self.observer.schedule(logging_handler, self.folder_path, recursive=False) # Optional
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
