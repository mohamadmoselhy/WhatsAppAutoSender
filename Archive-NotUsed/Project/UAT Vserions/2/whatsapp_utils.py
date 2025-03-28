"""
Author: Mohamed Ibrahim Moselhy
Role: Senior RPA Developer
Description:
    This module provides helper functions to automate interactions with WhatsApp Web.
    It includes functions for locating UI elements, sending messages, and handling file attachments.

Date: March 2025
"""

import time
import webbrowser
import pyautogui
import pygetwindow as gw
import pyperclip  # To handle Arabic text
import os
import ctypes
from input_control import block_input, unblock_input
from config import contact_name, icons, message

def locate_image(image_path, confidence=0.8, retries=5):
    """Attempts to locate an image on the screen with retries and exception handling."""
    
    if not os.path.exists(image_path):
        error_msg = f"[ERROR] Image file not found: {image_path}"
        print(error_msg)
        raise FileNotFoundError(error_msg)

    print(f"[INFO] Looking for image: {image_path} with confidence {confidence}")

    for attempt in range(retries):
        try:
            print(f"[DEBUG] Attempt {attempt + 1} to find {image_path}")
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if location:
                print(f"[SUCCESS] Found {image_path} at {location}")
                return location
        except pyautogui.ImageNotFoundException:
            print(f"[WARNING] Image not found: {image_path} (Attempt {attempt + 1})")
        except Exception as e:
            error_msg = f"[ERROR] Unexpected error while searching for {image_path}: {e}"
            print(error_msg)
            raise RuntimeError(error_msg) from e

        time.sleep(1)  # Wait before retrying

    error_msg = f"[ERROR] Failed to locate {image_path} after {retries} attempts."
    print(error_msg)
    raise TimeoutError(error_msg)

def clear_the_existing_data():
    """Clears the input field before entering new text."""
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    time.sleep(1)

def get_user_choice():
    """Ask the user whether to send a message with an attachment or only a message."""
    unblock_input()
    try:
        response = ctypes.windll.user32.MessageBoxW(
            0, "Do you want to send a message with an attachment?\nYes = With Attachment\nNo = Message Only",
            "Message Sending Option", 4
        )
        return response == 6  
    except Exception as e:
        error_msg = f"[ERROR] Error while getting user choice: {e}"
        print(error_msg)
        raise RuntimeError(error_msg) from e
    finally:
        block_input()

def open_whatsapp_chat():
    """Opens WhatsApp Web if not already open."""
    try:
        print("[INFO] Opening WhatsApp Web...")
        webbrowser.open("https://web.whatsapp.com/")
        time.sleep(15)  
        return True
    except Exception as e:
        error_msg = f"[ERROR] Failed to open WhatsApp Web: {e}"
        print(error_msg)
        raise RuntimeError(error_msg) from e

def ask_user_to_send_message():
    """Prompt the user to choose whether to send a message or skip."""
    unblock_input()
    try:
        response = ctypes.windll.user32.MessageBoxW(
            0, "Do you want to send a message?\nYes = Send\nNo = Skip",
            "Message Sending Option", 4  # 4 = Yes/No dialog
        )
        return response == 6  # Yes = 6 (Send), No = 7 (Skip)
    except Exception as e:
        print(f"[ERROR] Error while asking user to send message: {e}")
        return False
    finally:
        block_input()

def close_whatsapp_tab():
    """Closes the WhatsApp Web tab if it is open."""
    try:
        windows = gw.getWindowsWithTitle("WhatsApp")
        if windows:
            for win in windows:
                print(f"[INFO] Closing WhatsApp Web tab: {win.title}")
                win.close()
            return True
        else:
            print("[INFO] No WhatsApp Web tab found.")
            return False
    except Exception as e:
        error_msg = f"[ERROR] Failed to close WhatsApp Web tab: {e}"
        print(error_msg)
        raise RuntimeError(error_msg) from e

def write_in_field(name_field_image, text_value):    
    """Finds the contact search field and types the contact name."""
    try:
        print("[INFO] Searching for name field...")
        name_location = locate_image(name_field_image, confidence=0.5)
        
        if name_location:
            print(f"[INFO] Name field found at {name_location}. Clicking...")
            pyautogui.click(name_location)
            time.sleep(2)  # Allow field to focus
            
            print("[INFO] Clearing existing text...")
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')

            time.sleep(1)  # Extra delay before typing
            
            print(f"[INFO] Typing name: {text_value}")
            pyautogui.write(text_value, interval=0.1)
            pyautogui.press("enter")  
            time.sleep(3)
            print("[SUCCESS] Contact selected successfully!")
            return True 

        error_msg = "❌ Name field not found! Ensure WhatsApp Web is fully loaded."
        print(error_msg)
        raise ValueError(error_msg)
        
    except Exception as e:
        error_msg = f"[ERROR] Failed to write in field: {e}"
        print(error_msg)
        raise RuntimeError(error_msg) from e


def send_file(file_path):
    """Attaches and sends a file via WhatsApp."""
    try:
        print(f"[INFO] Attempting to send file: {file_path}")

        attachment_location = locate_image(icons["attachment"])
        if not attachment_location:
            raise FileNotFoundError("Attachment button not found.")

        pyautogui.click(attachment_location)
        time.sleep(2)
        print("[INFO] Clicked attachment button.")

        doc_location = locate_image(icons["document"])
        if not doc_location:
            raise FileNotFoundError("Document option not found.")

        pyautogui.click(doc_location)
        time.sleep(2)
        print("[INFO] Clicked document option.")

        time.sleep(2)
        print(f"[INFO] Pasting file path: {file_path}")
        pyperclip.copy(file_path)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(3)
        pyautogui.press("enter")
        print(f"✅ File '{file_path}' sent successfully!")
    except Exception as e:
        error_msg = f"[ERROR] Failed to send file: {e}"
        print(error_msg)
        raise RuntimeError(error_msg) from e

def send_message(message):
    """Sends a message to the selected WhatsApp contact."""
    try:
        print("[INFO] Attempting to send message...")
        msg_box = locate_image(icons["message_box"])
        if not msg_box:
            raise FileNotFoundError("Message box not found.")

        pyautogui.click(msg_box)
        time.sleep(1)
        print(f"[INFO] Pasting message: {message}")
        pyperclip.copy(message)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(2)
        print("✅ Message sent successfully!")
    except Exception as e:
        error_msg = f"[ERROR] Failed to send message: {e}"
        print(error_msg)
        raise RuntimeError(error_msg) from e
