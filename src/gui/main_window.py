"""
Main window for WhatsApp Auto Sender
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading

from src.core.config import config
from src.core.logger import logger
from src.core.file_watcher import FileWatcher
from src.whatsapp.sender import WhatsAppSender

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Auto Sender")
        self.root.geometry("800x600")
        
        self.sender = WhatsAppSender()
        self.watcher = None
        self.monitoring_thread = None
        
        self.create_widgets()
        
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
        self.status_label.config(text=message)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
    def process_file(self, file_path: str):
        try:
            self.update_status(f"Processing file: {file_path}")
            
            if self.sender.notify_file_ready(file_path):
                self.update_status(f"Successfully sent notification for file: {file_path}")
            else:
                self.update_status(f"Failed to send notification for file: {file_path}")
                
        except Exception as e:
            logger.log_error(e, f"Error processing file {file_path}")
            self.update_status(f"Error processing file: {file_path}")
            
    def start_monitoring(self):
        try:
            # Create file watcher
            self.watcher = FileWatcher(
                folder_path=config.folder_to_watch,
                callback=self.process_file
            )
            
            # Start monitoring
            self.monitoring_thread = threading.Thread(target=self.watcher.start)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            
            # Update UI
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.update_status(f"Monitoring folder: {config.folder_to_watch}")
            
        except Exception as e:
            logger.log_error(e, "Error starting monitoring")
            messagebox.showerror("Error", f"Failed to start monitoring: {str(e)}")
            
    def stop_monitoring(self):
        try:
            if self.watcher:
                self.watcher.stop()
                self.watcher = None
                
            if self.monitoring_thread:
                self.monitoring_thread.join()
                self.monitoring_thread = None
                
            # Update UI
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.update_status("Monitoring stopped")
            
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