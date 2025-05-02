"""
Author  : Mohamed Moselhy
Date    : May 1, 2025
Purpose : This script monitors a specific folder for new files and sends a WhatsApp notification
          when a new file is detected. It uses a retry mechanism for failed sends and captures
          a screenshot on failure for debugging purposes. The application runs continuously 
          until manually stopped.
Modules :
    - config: Contains configuration settings like folder paths.
    - logger: Handles logging of information and errors.
    - file_watcher: Watches a directory for new files.
    - sender: Sends WhatsApp messages using an internal API.
    - screenshot_utils: Takes screenshots on failure for diagnostics.
"""

# Importing required standard and custom modules
import os                    # For interacting with the operating system (like checking/creating directories)
import time                  # For handling time-based operations (like delays)
import sys                   # For system-level operations like exiting the script

# Importing internal project modules
from src.core.config import config                   # Configuration settings (e.g., folder paths)
from src.core.logger import logger                   # Custom logger for logging information and errors
from src.core.file_watcher import FileWatcher        # Class that monitors a folder for new files
from src.whatsapp.sender import WhatsAppSender       # Class responsible for sending WhatsApp messages
from src.core.screenshot_utils import take_screenshot  # Utility function for taking screenshots on error
from src.core.constants import MAX_RETRIES, RETRY_DELAY

def process_file(file_path: str):
    """
    Attempts to process a detected file by sending a WhatsApp notification.
    Retries up to MAX_RETRIES if an exception occurs, and logs the outcome.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.log_info(f"Processing file: {file_path} (Attempt {attempt})")
            sender = WhatsAppSender()
            if sender.notify_file_ready(file_path):
                logger.log_info(f"Successfully sent notification for file: {file_path}")
                break
            else:
                error_msg = f"Failed to send notification for file: {file_path}"
                logger.log_error(None, error_msg)
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                else:
                    take_screenshot("Error")
                    logger.log_error(None, error_msg)
        except Exception as e:
            logger.log_error(e, f"Error processing file {file_path} on attempt {attempt}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                take_screenshot("file_check_error")
                logger.log_error(e, f"All {MAX_RETRIES} attempts raised errors for file: {file_path}")

def main():
    """
    Initializes the folder watcher and keeps the application running indefinitely.
    Handles all exceptions gracefully and ensures the application never terminates unexpectedly.
    """
    while True:
        try:
            # Ensure the folder to watch exists
            if not os.path.exists(config.folder_to_watch):
                os.makedirs(config.folder_to_watch, exist_ok=True)
                logger.log_info(f"Created folder: {config.folder_to_watch}")

            # Initialize and start watching the folder
            watcher = FileWatcher(config.folder_to_watch, process_file)
            watcher.start()

            logger.log_info("WhatsApp Auto Sender started. Monitoring for files...")
            logger.log_info(f"Watching folder: {config.folder_to_watch}")
            logger.log_info("Press Ctrl+C to stop the application")

            # Keep the script running indefinitely
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.log_info("Stopping WhatsApp Auto Sender...")
            try:
                watcher.stop()
            except Exception:
                pass
            sys.exit(0)
        except Exception as e:
            logger.log_error(e, "Unhandled exception in main loop. Application will recover and continue running.")
            time.sleep(5)  # Wait a bit before retrying the main loop

# Entry point of the script
if __name__ == "__main__":
    main()
