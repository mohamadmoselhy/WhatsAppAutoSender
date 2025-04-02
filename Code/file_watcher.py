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
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileAddedHandler(FileSystemEventHandler):
    """Handles newly created files in the watched directory."""

    def __init__(self, event):
        """Initializes the event handler for file monitoring."""
        try:
            super().__init__()
            self.new_file_path = None
            self.event = event  # Synchronization event to notify the main thread
        except Exception as e:
            error_msg = f"⚠️ Error initializing FileAddedHandler: {e}"
            print(error_msg)
            raise RuntimeError(error_msg) from e  # Rethrow for higher-level handling

    def on_created(self, event):
        """Handles newly created files in the watched directory."""
        try:
            if not event.is_directory:  # Ignore folder creation events
                self.new_file_path = os.path.abspath(event.src_path)
                print(f"📂 New file detected: {self.new_file_path}")
                self.event.set()  # Signal the main thread to proceed
        except Exception as e:
            error_msg = f"⚠️ Error processing file creation event: {e}"
            print(error_msg)
            raise RuntimeError(error_msg) from e  # Rethrow for debugging or higher-level handling

def monitor_folder(folder_to_watch):
    """Monitors a folder for new files and returns the detected file path."""
    try:
        previous_files = get_all_files(folder_to_watch)
        print(f"👀 Monitoring folder: {folder_to_watch}")
        
        while True:
            time.sleep(5)  # Check every 5 seconds
            current_files = get_all_files(folder_to_watch)
            new_files = current_files - previous_files
            
            if new_files:
                for file in new_files:
                    print(f"📂 New file detected: {file}")
                    return file  # Return the first detected new file
            
            previous_files = current_files
    
    except KeyboardInterrupt:
        print("🛑 Stopping file watcher...")
        return None
    except Exception as e:
        error_msg = f"⚠️ Unexpected error in monitor_folder: {e}"
        print(error_msg)
        raise RuntimeError(error_msg) from e  # Rethrow to allow higher-level handling

def get_all_files(folder_path):
    try:
        file_paths = set()
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_paths.add(os.path.join(root, file))
        return file_paths
    except Exception as e:
        print(f"Error while scanning files: {e}")
        raise