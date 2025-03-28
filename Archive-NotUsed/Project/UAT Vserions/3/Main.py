"""
Author: Mohamed Ibrahim Moselhy
Role: Senior RPA Developer
Description: 
    This script monitors a specified folder for new files and sends them via WhatsApp. 
    It blocks user input during the process to prevent interference and ensures successful 
    file transmission using WhatsApp automation.

Date: March 2025
"""

# Import necessary modules for folder monitoring, WhatsApp file sending, user interaction, and input control.
try:
    from file_watcher import monitor_folder  # Monitors a specified folder for new files.
    from whatsapp_sender import send_file_via_whatsapp  # Handles sending files via WhatsApp.
    from whatsapp_utils import ask_user_to_send_message, close_whatsapp_tab  # Prompts the user for confirmation before sending.
    from input_control import block_input, unblock_input  # Blocks and unblocks user input during execution.
    import tkinter as tk
    from tkinter import messagebox
    from config import folder_to_watch  # Imports the folder path to be monitored.
except ModuleNotFoundError as e:
    error_message = (
        f"Error: Missing module - {e.name}\n"
        "Please install the required dependencies or contact the administrator for support."
    )
    print(error_message)
    messagebox.showerror("Import Error", error_message)
    exit(1) 



# Infinite loop to continuously monitor the folder for new files.
while True:
    try:
        print("👀 Monitoring folder for new files...")
        detected_file_path = monitor_folder(folder_to_watch)  # Check for a new file in the monitored folder.

        if detected_file_path:  # If a new file is detected:
            print(f"📂 New file detected: {detected_file_path}")
            block_input()  # Block user input to prevent interference.

            if ask_user_to_send_message():  # Ask user for confirmation to send the file.
                file_sent_successfully = send_file_via_whatsapp(detected_file_path)  # Send the file via WhatsApp.

                if file_sent_successfully:  # If the file is successfully sent:
                    print("✅ File sent successfully via WhatsApp.")
                else:  # If sending fails:
                    raise RuntimeError("Failed to send the file via WhatsApp.")
        else:  # If no file is detected or monitoring is interrupted:
            raise RuntimeError("No file detected or monitoring was interrupted.")
        unblock_input()  # Ensure user input is always unblocked after the process.

    except KeyboardInterrupt:
        print("🛑 Script stopped by user.")
        break  # Exit the loop cleanly when interrupted.

    except Exception as e:  # Catch any unexpected errors
        unblock_input()
        error_msg = f"⚠️ An error occurred: {e}"
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror("Error", error_msg)
  # Rethrow for higher-level handling.

    finally:
        try:
            close_whatsapp_tab()
        except Exception as e:
            print(f"⚠️ Failed to unblock input: {e}")

            # Initialize a hidden Tkinter window
            root = tk.Tk()
            root.withdraw()  # Hide the root window

            # Show the error message in a message box
            messagebox.showerror("Critical Failure", f"Unable to unblock user input.\nError: {e}")

            root.destroy()  # Close the Tkinter window
