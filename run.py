
"""
WhatsApp Auto Sender - Direct File Sender
Automatically monitors folder and sends files via WhatsApp
"""

import os
import time
import sys
from src.core.config import config
from src.core.logger import logger
from src.core.file_watcher import FileWatcher
from src.whatsapp.sender import WhatsAppSender

def process_file(file_path: str):
    """Process a file by sending it via WhatsApp with retry mechanism"""
    max_retries = 5
    delay_seconds = 5

    for attempt in range(1, max_retries + 1):
        try:
            logger.log_info(f"Processing file: {file_path} (Attempt {attempt})")

            # Send the file notification
            sender = WhatsAppSender()
            if sender.notify_file_ready(file_path):
                logger.log_info(f"Successfully sent notification for file: {file_path}")
                break  # Success, exit the loop
            else:
                logger.log_error(None, f"Failed to send notification for file: {file_path}")
                if attempt < max_retries:
                    time.sleep(delay_seconds)
                else:
                    logger.log_error(None, f"All {max_retries} attempts failed for file: {file_path}")

        except Exception as e:
            logger.log_error(e, f"Error processing file {file_path} on attempt {attempt}")
            if attempt < max_retries:
                time.sleep(delay_seconds)
            else:
                logger.log_error(e, f"All {max_retries} attempts raised errors for file: {file_path}")

def main():
    """Main function to start the file watcher"""
    try:
        # Create the folder if it doesn't exist
        if not os.path.exists(config.folder_to_watch):
            os.makedirs(config.folder_to_watch, exist_ok=True)
            logger.log_info(f"Created folder: {config.folder_to_watch}")

        # Create and start the file watcher
        watcher = FileWatcher(config.folder_to_watch, process_file)
        watcher.start()
        
        logger.log_info("WhatsApp Auto Sender started. Monitoring for files...")
        logger.log_info(f"Watching folder: {config.folder_to_watch}")
        logger.log_info("Press Ctrl+C to stop the application")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.log_info("Stopping WhatsApp Auto Sender...")
            watcher.stop()
            sys.exit(0)
            
    except Exception as e:
        logger.log_error(e, "Error in main function")
        sys.exit(1)

if __name__ == "__main__":
    main() 