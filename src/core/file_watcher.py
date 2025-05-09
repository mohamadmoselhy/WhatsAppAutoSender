"""
File watcher module for monitoring directory changes
"""

import os
import time
from pathlib import Path
from typing import Callable
from src.core.config import config
from src.core.constants import *
from src.core.logger import logger

class FileWatcher:
    def __init__(self, directory: str, callback: Callable[[str], None]):
        """
        Initialize file watcher
        
        Args:
            directory: Directory to watch
            callback: Function to call when a file is found. This should be a function
                     that processes the file, such as sending it via WhatsApp.
        """
        self.directory = Path(directory)
        self.callback = callback
        self.running = False
        self.processed_files = set()
        logger.log_info(f"File watcher initialized for directory: {directory}")

    def start(self):
        """Start watching the directory"""
        try:
            if not self.directory.exists():
                logger.log_error(None, f"Directory does not exist: {self.directory}")
                return

            self.running = True
            logger.log_info("File watcher started")
            
            while self.running:
                try:
                    self._check_files()
                    time.sleep(FILE_CHECK_INTERVAL)
                except Exception as e:
                    logger.log_error(e, "Error in file watcher loop")
                    time.sleep(ERROR_WAIT_TIME)
                    continue
                    
        except Exception as e:
            logger.log_error(e, "Failed to start file watcher")
            raise

    def stop(self):
        """Stop watching the directory"""
        self.running = False
        logger.log_info("File watcher stopped")

    def _is_file_ready(self, file_path: str) -> bool:
        """Check if a file is ready to be processed (not being written to)"""
        try:
            # Try to open the file in exclusive mode
            with open(file_path, 'rb') as f:
                return True
        except IOError:
            return False

    def _process_file(self, file_path: str) -> bool:
        """Process a single file"""
        try:
            return self.callback(file_path)
        except Exception as e:
            logger.log_error(e, f"Error processing file {file_path}")
            return False

    def _check_files(self) -> None:
        """Check for new files in the directory"""
        try:
            current_time = time.time()
            
            # Recursively get all subfolders
            subfolders = []
            for root, dirs, _ in os.walk(self.directory):
                for dir_name in dirs:
                    subfolders.append(Path(root) / dir_name)
            
            logger.log_debug(f"Found {len(subfolders)} subfolders in {self.directory}")
            
            # Check each subfolder
            for subfolder in subfolders:
                try:
                    # Check each file pattern in the subfolder
                    for pattern in FILE_PATTERNS:
                        for file_path in subfolder.glob(pattern):
                            try:
                                # Skip if file is too old
                                file_age = current_time - file_path.stat().st_mtime
                                if file_age > MAX_FILE_AGE:
                                    logger.log_debug(f"Skipping old file: {file_path} (age: {file_age:.1f}s)")
                                    continue

                                # Skip if already processed
                                if str(file_path) in self.processed_files:
                                    continue
                                
                                # Process the file
                                logger.log_info(f"Found new file in subfolder: {file_path}")
                                try:
                                    self.callback(str(file_path))
                                    self.processed_files.add(str(file_path))
                                    logger.log_info(f"File processed successfully: {file_path}")
                                except Exception as e:
                                    logger.log_error(e, f"Failed to process file: {file_path}")
                                    # Continue to next file instead of raising the exception
                                    continue
                                
                            except Exception as e:
                                logger.log_error(e, f"Error checking file: {file_path}")
                                # Continue to next file instead of raising the exception
                                continue
                            
                except Exception as e:
                    logger.log_error(e, f"Error checking subfolder: {subfolder}")
                    # Continue to next subfolder instead of raising the exception
                    continue
                
        except Exception as e:
            logger.log_error(e, "Error in file checking process")
            # Don't raise the exception, just log it and continue
            return
