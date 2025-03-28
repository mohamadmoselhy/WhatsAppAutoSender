"""
Author: Mohamed Ibrahim Moselhy
Role: Senior RPA Developer
Description: 
    Automates the process of sending messages and files via WhatsApp Web.
    It interacts with the WhatsApp interface using pyautogui and handles errors gracefully.

Date: March 2025
"""

import pyautogui
import time
import webbrowser  # To open WhatsApp Web
import ctypes  # For popup messages
import json
from config import contact_name, message, icons
from whatsapp_utils import (
    get_user_choice, send_file, write_in_field, locate_image, 
    clear_the_existing_data, open_whatsapp_chat, send_message, close_whatsapp_tab
)

def send_file_via_whatsapp(file_path):
    """Handles sending a message and optionally sending a file via WhatsApp Web."""
    try:
        print("[INFO] Starting WhatsApp automation...")

        # 1- Open WhatsApp
        if not open_whatsapp_chat():
            raise RuntimeError("Failed to open WhatsApp chat.")

        # 2- Search for the Contact
        if not write_in_field(icons["name_field"], contact_name):
            raise ValueError("Failed to search for contact on WhatsApp chat.")

        # 3- Ask the user whether to send a message only or include an attachment
        try:
            message_with_attachment = get_user_choice()
        except Exception as e:
            raise RuntimeError(f"Failed to get user choice: {e}") from e

        print(f"[INFO] User selected {'Message + File' if message_with_attachment else 'Message Only'} mode.")

        # 4- Send the message
        try:
            send_message(message)
        except Exception as e:
            raise RuntimeError(f"Failed to send message: {e}") from e

        # 5- If the user wants to send a file, handle the file upload
        if message_with_attachment:
            try:
                send_file(file_path)
            except Exception as e:
                raise RuntimeError(f"Failed to send file: {e}") from e

        # 6- Close the WhatsApp Web tab
        try:
            time.sleep(10)  # Wait before retrying
            close_whatsapp_tab()
        except Exception as e:
            raise RuntimeError(f"Failed to close WhatsApp tab: {e}") from e
        
        print("✅ WhatsApp message sent successfully.")
        return True

    except Exception as e:
        error_msg = f"⚠️ Error in send_file_via_whatsapp: {e}"
        print(error_msg)
        raise RuntimeError(error_msg) from e  # Rethrow for higher-level handling
