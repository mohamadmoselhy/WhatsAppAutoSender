"""
Author: Mohamed Ibrahim Moselhy
Role: Senior RPA Developer
Description:
    This module provides helper functions to automate interactions with WhatsApp Web.
    It includes functions for locating UI elements, sending messages, and handling file attachments.

Date: March 2025
"""

import time
import subprocess
import webbrowser
import pyautogui
import pygetwindow as gw
import pyperclip
import os
import sys
import ctypes
import logging
from input_control import block_input, unblock_input
from bidi.algorithm import get_display
from config import folder_to_watch, contact_name, message, name_field, name_field2, attachment, document, whatsapp_images, message_box

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler("logs/whatsapp_automation.log", mode='a')
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def locate_image(image_path, confidence=0.8, retries=5):
    if not os.path.exists(image_path):
        logger.error(f"Image file not found: {image_path}")
        raise FileNotFoundError(f"Image file not found: {image_path}")

    logger.info(f"Looking for image: {image_path} with confidence {confidence}")
    for attempt in range(retries):
        try:
            logger.debug(f"Attempt {attempt + 1} to find {image_path}")
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if location:
                logger.info(f"Found {image_path} at {location}")
                return location
        except Exception as e:
            logger.exception(f"Unexpected error while searching for {image_path}")
            raise RuntimeError(f"Unexpected error while searching for {image_path}: {e}") from e
        time.sleep(1)

    logger.error(f"Failed to locate {image_path} after {retries} attempts.")
    raise TimeoutError(f"Failed to locate {image_path} after {retries} attempts.")

def clear_the_existing_data():
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    time.sleep(1)

def get_user_choice():
    unblock_input()
    try:
        response = ctypes.windll.user32.MessageBoxW(
            0, "Do you want to send a message with an attachment?\nYes = With Attachment\nNo = Message Only",
            "Message Sending Option", 4
        )
        return response == 6
    except Exception as e:
        logger.exception("Error while getting user choice")
        raise RuntimeError("Error while getting user choice") from e
    finally:
        block_input()

def open_whatsapp_chat():
    try:
        logger.info("Opening WhatsApp Web in a new, maximized window in Microsoft Edge...")
        subprocess.run(["start", "msedge", "--new-window", "https://web.whatsapp.com/"], shell=True)
        time.sleep(15)
        pyautogui.hotkey('alt', 'space')
        time.sleep(1)
        pyautogui.press('x')
        return True
    except Exception as e:
        logger.exception("Failed to open WhatsApp Web")
        raise RuntimeError("Failed to open WhatsApp Web") from e

def ask_user_to_send_message():
    unblock_input()
    try:
        if sys.platform != "win32":
            raise OSError("MessageBoxW is only supported on Windows.")

        response = ctypes.windll.user32.MessageBoxW(
            0, "Do you want to send a message?\nYes = Send\nNo = Skip",
            "Message Sending Option", 4
        )
        return response == 6
    except Exception as e:
        logger.exception("Error while asking user to send message")
        raise
    finally:
        block_input()

def close_whatsapp_tab():
    try:
        windows = gw.getWindowsWithTitle("WhatsApp")
        if not windows:
            logger.info("No WhatsApp Web tab found.")
            return False

        for win in windows:
            if "WhatsApp Web" in win.title or "WhatsApp" in win.title:
                logger.info(f"Closing WhatsApp Web tab: {win.title}")
                win.close()
                return True

        logger.info("No WhatsApp Web browser tab found.")
        return False

    except Exception as e:
        logger.exception("Failed to close WhatsApp Web tab")
        raise RuntimeError("Failed to close WhatsApp Web tab") from e

def write_in_field(name_field_image, text_value):
    try:
        logger.info("Searching for name field...")
        name_location = locate_image(name_field_image, confidence=0.5)

        if name_location:
            logger.info(f"Name field found at {name_location}. Clicking...")
            pyautogui.click(name_location)
            time.sleep(2)

            logger.info("Clearing existing text...")
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            time.sleep(1)

            logger.info(f"Pasting name: {text_value}")
            pyperclip.copy(text_value)
            pyautogui.hotkey("ctrl", "v")
            pyautogui.press("enter")
            time.sleep(3)
            logger.info("Contact selected successfully.")
            return True

        logger.error("Name field not found. Ensure WhatsApp Web is fully loaded.")
        raise ValueError("Name field not found.")

    except Exception as e:
        logger.exception("Failed to write in field")
        raise RuntimeError("Failed to write in field") from e

def send_file(file_path):
    try:
        logger.info(f"Attempting to send file: {file_path}")
        attachment_location = locate_image(attachment)
        if not attachment_location:
            raise FileNotFoundError("Attachment button not found.")

        pyautogui.click(attachment_location)
        time.sleep(2)
        logger.info("Clicked attachment button.")

        doc_location = locate_image(document)
        if not doc_location:
            raise FileNotFoundError("Document option not found.")

        pyautogui.click(doc_location)
        time.sleep(2)
        logger.info("Clicked document option.")

        time.sleep(2)
        logger.info(f"Pasting file path: {file_path}")
        pyperclip.copy(file_path)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(3)
        pyautogui.press("enter")
        logger.info(f"File '{file_path}' sent successfully.")
    except Exception as e:
        logger.exception("Failed to send file")
        raise RuntimeError("Failed to send file") from e

def send_message(message):
    try:
        logger.info("Attempting to send message...")
        msg_box = locate_image(message_box)
        if not msg_box:
            raise FileNotFoundError("Message box not found.")

        pyautogui.click(msg_box)
        time.sleep(1)
        logger.info(f"Pasting message: {message}")
        pyperclip.copy(message)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(2)
        logger.info("Message sent successfully.")
    except Exception as e:
        logger.exception("Failed to send message")
        raise RuntimeError("Failed to send message") from e
