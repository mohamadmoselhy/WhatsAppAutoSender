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
from file_watcher import monitor_folder  # Monitors a specified folder for new files.
from whatsapp_sender import send_file_via_whatsapp  # Handles sending files via WhatsApp.
from whatsapp_utils import ask_user_to_send_message  # Prompts the user for confirmation before sending.
from input_control import block_input, unblock_input  # Blocks and unblocks user input during execution.
from config import folder_to_watch  # Imports the folder path to be monitored.


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

    except KeyboardInterrupt:
        print("🛑 Script stopped by user.")
        break  # Exit the loop cleanly when interrupted.

    except Exception as e:  # Catch any unexpected errors
        error_msg = f"⚠️ An error occurred: {e}"
        print(error_msg)
        raise RuntimeError(f"[Fetal] {error_msg}") from e  # Correct
  # Rethrow for higher-level handling.

    finally:
        try:
            unblock_input()  # Ensure user input is always unblocked after the process.
        except Exception as e:
            print(f"⚠️ Failed to unblock input: {e}")
            raise RuntimeError("Critical failure: Unable to unblock user input.") from e
