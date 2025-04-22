"""
Main window for WhatsApp Auto Sender
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import time
import re # Import re for temporary file check
from pathlib import Path

from src.core.config import config
from src.core.logger import logger
from src.whatsapp.sender import WhatsAppSender

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Auto Sender")
        self.root.geometry("800x600")
        
        self.sender = WhatsAppSender()
        self.monitoring_thread = None
        self.monitoring_active = False # Flag to control the polling loop
        self.known_files = set() # Store the set of files from the previous scan
        
        self.create_widgets()
        
    def is_temporary_file(self, file_path: str) -> bool:
        """Check if the file is likely a temporary file (moved logic here)"""
        if not file_path:
            return False
        file_name = os.path.basename(file_path)
        if not file_name:
            return False

        # More specific Excel temporary file patterns
        temp_patterns = [
            r'^~\$.*\.xlsx$',           # Excel lock files (e.g., ~$Document.xlsx)
            r'^~.*\.tmp$',              # Starts with ~, ends with .tmp
            r'^[0-9A-F]{8}$',           # Often 8-hex-char temp files in the same folder
            r'.*\.tmp$',                # Ends with .tmp
            r'.*\.TMP$',                # Ends with .TMP
            r'.*\.xlsx~RF[0-9a-f]+\.TMP$' # Excel autosave/recovery pattern
        ]

        for pattern in temp_patterns:
            if re.match(pattern, file_name, re.IGNORECASE):
                logger.log_info(f"Detected temporary file pattern: {file_name}")
                return True
        return False

    def is_file_stable(self, file_path: str) -> bool:
         """Check if the file seems stable (exists, size not changing rapidly)."""
         if not os.path.exists(file_path):
             return False
         try:
             initial_size = os.path.getsize(file_path)
             time.sleep(0.5) # Wait a short period
             if not os.path.exists(file_path): # Check again if deleted during sleep
                 return False
             current_size = os.path.getsize(file_path)
             return initial_size == current_size and current_size > 0 # Ensure size is stable and not empty
         except OSError as e:
             logger.log_error(e, f"Error checking stability for {file_path}, likely still locked.")
             return False
         except Exception as e:
              logger.log_error(e, f"Unexpected error during stability check for {file_path}")
              return False

    def create_widgets(self):
        # Status frame
        status_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Not monitoring")
        self.status_label.pack(side=tk.LEFT)
        
        # Activity log
        log_frame = ttk.LabelFrame(self.root, text="Activity Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.log_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
        # Control buttons
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_button = ttk.Button(button_frame, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop Monitoring", command=self.stop_monitoring)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.stop_button.config(state=tk.DISABLED)
        
    def update_status(self, message: str):
        # Ensure UI updates happen on the main thread
        self.root.after(0, lambda: self._update_status_ui(message))

    def _update_status_ui(self, message: str):
        """Helper to update UI elements"""
        self.status_label.config(text=message)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END) # Auto-scroll
        
    def process_file(self, file_path: str):
        """Process a single file (called by the monitoring loop)"""
        try:
            # This log now happens in the polling loop before calling process_file
            # self.update_status(f"Processing file: {file_path}")

            # Perform the sending action
            if self.sender.notify_file_ready(file_path):
                self.update_status(f"Successfully sent notification for file: {os.path.basename(file_path)}")
            else:
                self.update_status(f"Failed to send notification for file: {os.path.basename(file_path)}")

        except Exception as e:
            logger.log_error(e, f"Error processing file {file_path}")
            self.update_status(f"Error processing file: {os.path.basename(file_path)}")

    def monitor_folder_loop(self):
        """The actual polling logic run in a separate thread"""
        polling_interval = 5 # Check every 5 seconds (adjust as needed)
        logger.log_info("Polling thread started.")

        while self.monitoring_active:
            try:
                current_files = set()
                folder_path = config.folder_to_watch
                if os.path.isdir(folder_path):
                     # List files, not directories, directly in the target folder
                    current_files = {
                        os.path.join(folder_path, f)
                        for f in os.listdir(folder_path)
                        if os.path.isfile(os.path.join(folder_path, f))
                    }
                else:
                    logger.log_warning(f"Monitored folder does not exist or is not a directory: {folder_path}")
                    # Optionally stop monitoring if folder disappears
                    # self.stop_monitoring() # Consider implications
                    time.sleep(polling_interval)
                    continue # Skip to next iteration


                # Find newly added files (in current but not in known)
                newly_added_files = current_files - self.known_files

                if newly_added_files:
                    logger.log_info(f"Detected {len(newly_added_files)} new file(s): {[os.path.basename(f) for f in newly_added_files]}")

                    for file_path in newly_added_files:
                        file_name = os.path.basename(file_path)
                        logger.log_info(f"Checking new file: {file_name}")

                        # 1. Filter out temporary files
                        if self.is_temporary_file(file_path):
                            logger.log_info(f"Skipping temporary file: {file_name}")
                            # Add temporary files to known_files immediately so we don't re-check them
                            self.known_files.add(file_path)
                            continue

                        # 2. Check for stability
                        if not self.is_file_stable(file_path):
                            logger.log_info(f"Skipping unstable/inaccessible file: {file_name}")
                            # Don't add to known_files yet, might become stable later
                            continue

                        # 3. If passes checks, process it
                        logger.log_info(f"File '{file_name}' passed checks. Queueing for processing.")
                        self.update_status(f"Processing file: {file_name}") # Update status before calling process
                        # Call process_file (runs sender logic)
                        self.process_file(file_path)
                        # Add successfully processed file to known_files
                        self.known_files.add(file_path)


                # Update the set of known files for the next iteration
                # Important: update known_files *after* processing loop to handle files added *during* the loop correctly
                # However, we need to add *all* current files, not just the processed ones,
                # otherwise deleted files are never removed from known_files.
                self.known_files = current_files

                # Wait for the next poll
                time.sleep(polling_interval)

            except Exception as e:
                logger.log_error(e, "Error in monitoring loop")
                # Add a small delay to prevent rapid-fire errors in case of persistent issues
                time.sleep(polling_interval)

        logger.log_info("Polling thread finished.")


    def start_monitoring(self):
        try:
            folder_path = config.folder_to_watch
            if not os.path.isdir(folder_path):
                 messagebox.showerror("Error", f"Folder not found or not a directory: {folder_path}")
                 return

            # Get the initial set of files (excluding temporary ones)
            self.known_files = {
                os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f)) # and not self.is_temporary_file(os.path.join(folder_path, f)) # Option: prime known_files without temps
            }
            logger.log_info(f"Initial files in folder: {len(self.known_files)}")

            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(target=self.monitor_folder_loop, daemon=True)
            self.monitoring_thread.start()

            # Update UI
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.update_status(f"Monitoring folder: {folder_path}")

        except Exception as e:
            logger.log_error(e, "Error starting monitoring")
            messagebox.showerror("Error", f"Failed to start monitoring: {str(e)}")

    def stop_monitoring(self):
        try:
            if self.monitoring_thread and self.monitoring_active:
                logger.log_info("Stopping monitoring thread...")
                self.monitoring_active = False
                # Wait for the thread to finish its current loop iteration
                self.monitoring_thread.join(timeout=10) # Wait up to 10 seconds
                if self.monitoring_thread.is_alive():
                     logger.log_warning("Monitoring thread did not stop gracefully.")
                self.monitoring_thread = None
                logger.log_info("Monitoring stopped.")

            # Update UI
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.update_status("Monitoring stopped")
            # Clear known files when stopping
            self.known_files = set()


        except Exception as e:
            logger.log_error(e, "Error stopping monitoring")
            messagebox.showerror("Error", f"Failed to stop monitoring: {str(e)}")

    def on_closing(self):
        try:
            self.stop_monitoring()
            self.root.destroy()
        except Exception as e:
            logger.log_error(e, "Error closing application")
            self.root.destroy() 