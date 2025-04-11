import logging
import os
from datetime import datetime
import pyautogui
import traceback
import tkinter as tk
from tkinter import messagebox

# Set up logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"app_log_{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    filename=log_file,
    filemode='a',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Starting the WhatsApp file automation script.")

# Function to take a screenshot
def take_screenshot(error_message):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_filename = f"screenshot_{timestamp}.png"
    
    # Capture screenshot
    screenshot = pyautogui.screenshot()
    
    # Create a directory to save screenshots if it doesn't exist
    if not os.path.exists("error_screenshots"):
        os.makedirs("error_screenshots")
    
    # Save screenshot
    screenshot.save(os.path.join("error_screenshots", screenshot_filename))
    
    # Log the error message with timestamp
    with open("error_screenshots/error_log.txt", "a") as log_file:
        log_file.write(f"{timestamp} - Error: {error_message}\n")

try:
    from config import folder_to_watch
    from file_watcher import monitor_folder
    from whatsapp_sender import send_file_via_whatsapp
    from whatsapp_utils import ask_user_to_send_message, close_whatsapp_tab
    from input_control import block_input, unblock_input

except ModuleNotFoundError as e:
    error_message = (
        f"Error: Missing module - {e.name}\n"
        "Please install the required dependencies or contact the administrator for support."
    )
    logging.critical(error_message)
    take_screenshot(error_message)  # Take screenshot in case of error
    messagebox.showerror("Import Error", error_message)
    exit(1)

# Infinite loop to monitor folder
while True:
    try:
        logging.info("Monitoring folder for new files...")
        detected_file_path = monitor_folder(folder_to_watch)

        if detected_file_path:
            logging.info(f"New file detected: {detected_file_path}")
            block_input()
            logging.info("User input blocked.")

            if ask_user_to_send_message():
                logging.info("User confirmed to send the file.")
                file_sent_successfully = send_file_via_whatsapp(detected_file_path)

                if file_sent_successfully:
                    logging.info("File sent successfully via WhatsApp.")
                else:
                    raise RuntimeError("Failed to send the file via WhatsApp.")
            else:
                logging.info("User declined to send the file.")

            unblock_input()
            logging.info("User input unblocked.")
        else:
            raise RuntimeError("No file detected or monitoring was interrupted.")

    except KeyboardInterrupt:
        logging.info("Script stopped by user via KeyboardInterrupt.")
        break

    except Exception as e:
        unblock_input()
        error_msg = f"An error occurred: {e}"
        logging.exception(error_msg)
        take_screenshot(error_msg)  # Take screenshot in case of error
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", error_msg)

    finally:
        try:
            close_whatsapp_tab()
            logging.info("WhatsApp tab closed successfully.")
        except Exception as e:
            logging.exception("Failed to close WhatsApp tab.")
            take_screenshot(f"Critical failure: Unable to close WhatsApp tab. Error: {e}")  # Take screenshot for critical failure
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Critical Failure", f"Unable to unblock user input.\nError: {e}")
            root.destroy()
