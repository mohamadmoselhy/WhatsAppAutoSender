"""
WhatsApp Auto Sender main application
"""

import tkinter as tk
from src.gui.main_window import MainWindow
from src.core.logger import logger

def main():
    try:
        # Create root window
        root = tk.Tk()
        
        # Create main window
        app = MainWindow(root)
        
        # Bind close event
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Start main loop
        root.mainloop()
        
    except Exception as e:
        logger.log_error(e, "Error in main application")
        raise

if __name__ == "__main__":
    main() 