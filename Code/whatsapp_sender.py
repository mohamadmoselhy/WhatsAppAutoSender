"""
Author: Mohamed Ibrahim Moselhy
Role: Senior RPA Developer
Description: 
    Automates the process of sending messages and files via WhatsApp Web.
    It interacts with the WhatsApp interface using pyautogui and handles errors gracefully.

Date: March 2025
"""

import time
import os
import sys
import io
import logging
from config import folder_to_watch, contact_name, message, name_field, name_field2, attachment, document, whatsapp_images, message_box
from whatsapp_utils import (
    get_user_choice, send_file, write_in_field, locate_image, 
    clear_the_existing_data, open_whatsapp_chat, send_message, close_whatsapp_tab
)

# Ensure stdout supports UTF-8 for Arabic names in logs
if sys.stdout and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configure logging (file + console with UTF-8 support)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("whatsapp_automation.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def get_Contact_name(path, keyword="منظورة تجربة"):
    parts = path.split(os.sep)
    if keyword in parts:
        index = parts.index(keyword)
        if index + 1 < len(parts):
            return parts[index + 1]
    return None

def send_file_via_whatsapp(file_path):
    """Handles sending a message and optionally sending a file via WhatsApp Web."""
    try:
        logger.info("Starting WhatsApp automation...")

        # 1- Open WhatsApp
        if not open_whatsapp_chat():
            raise RuntimeError("Failed to open WhatsApp chat.")

        # 2- Search for the Contact
        contact_name = get_Contact_name(file_path)
        if not write_in_field(name_field, contact_name):
            raise ValueError("Failed to search for contact on WhatsApp chat.")

        # 3- Ask user whether to send message only or include file
        try:
            message_with_attachment = get_user_choice()
        except Exception as e:
            raise RuntimeError(f"Failed to get user choice: {e}") from e

        logger.info("User selected mode: %s", "Message + File" if message_with_attachment else "Message Only")

        # 4- Send the message
        try:
            send_message(message)
        except Exception as e:
            raise RuntimeError(f"Failed to send message: {e}") from e

        # 5- Send file if needed
        if message_with_attachment:
            try:
                send_file(file_path)
            except Exception as e:
                raise RuntimeError(f"Failed to send file: {e}") from e

        # 6- Close WhatsApp Web tab
        try:
            time.sleep(10)
            close_whatsapp_tab()
        except Exception as e:
            raise RuntimeError(f"Failed to close WhatsApp tab: {e}") from e

        logger.info("WhatsApp message sent successfully.")
        return True

    except Exception as e:
        error_msg = f"Error in send_file_via_whatsapp: {e}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e
