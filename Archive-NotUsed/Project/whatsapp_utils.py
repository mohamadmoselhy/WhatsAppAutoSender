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
import time
import pyautogui
import pygetwindow as gw
import pyperclip  # To handle Arabic text
import os
import ctypes
from input_control import block_input, unblock_input
from config import load_config

ConfigDic=load_config()

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
    """Opens WhatsApp Web if not already open and maximizes the browser window."""
    try:
        print("[INFO] Opening WhatsApp Web...")
        webbrowser.open("https://web.whatsapp.com/")
        
        # Wait for the page to load completely
        time.sleep(15)  # Adjust the sleep time if necessary
        
        # Find the browser window with 'WhatsApp' in the title
        window_title = 'WhatsApp'  # Change this if the browser title differs
        
        # Try to find and maximize the window
        windows = gw.getWindowsWithTitle(window_title)
        
        if windows:
            window = windows[0]  # Get the first window that matches the title
            window.maximize()  # Maximize the window
            print("[INFO] WhatsApp Web is now maximized.")
        else:
            print("[WARNING] WhatsApp Web window not found.")
        
        return window

    except Exception as e:
        error_msg = f"[ERROR] Failed to open or maximize WhatsApp Web: {e}"
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

def write_in_field(page, element_type, element_value, text_value):    
    """Finds the contact search field and types the contact name."""
    try:
        print("[INFO] Searching for name field...")
        name_location = click_selector(page, element_type, element_value)
        
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

        attachment_location = locate_image(ConfigDic.get("attachment"))
        if not attachment_location:
            raise FileNotFoundError("Attachment button not found.")

        pyautogui.click(attachment_location)
        time.sleep(2)
        print("[INFO] Clicked attachment button.")

        doc_location = locate_image(ConfigDic.get("document"))
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

def send_message(Page,message):
    """Sends a message to the selected WhatsApp contact."""
    try:
        print("[INFO] Attempting to send message...")
        ClickOnMessageField = click_selector(Page,ConfigDic.get("TypeMessageField_Type"),ConfigDic.get("TypeMessageField"))
        
        if not ClickOnMessageField :
            raise FileNotFoundError("Message box not found.")

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

async def click_selector(page, element_type, element_value):
    """Clicks on the specified element based on the provided selector type."""
    try:
        # Determine the correct selector format
        selector = ""
        if element_type.tolower() == "class":
            selector = f".{element_value}"  # Class selector (e.g., ".button")
        elif element_type.tolower() == "id":
            selector = f"#{element_value}"  # ID selector (e.g., "#submit")
        elif element_type.tolower() == "css":
            selector = element_value  # Direct CSS selector (e.g., "button.submit")
        else:
            raise ValueError("Invalid selector type. Use 'class', 'id', or 'css'.")

        await page.waitForSelector(selector, timeout=5000)  # Ensure element is loaded
        await page.click(selector)  # Click the element
        print(f"Clicked on element: {selector}")
        return True
    except Exception as e:
        print(f"Error clicking element ({element_type}: {element_value}): {e}")
        return False

async def type_text(page, element_type, element_value, text):
    """Types text into the specified element based on the provided selector type."""
    try:
        # Determine the correct selector format
        selector = ""
        if element_type.lower() == "class":
            selector = f".{element_value}"  # Class selector (e.g., ".input-field")
        elif element_type.lower() == "id":
            selector = f"#{element_value}"  # ID selector (e.g., "#username")
        elif element_type.lower() == "css":
            selector = element_value  # Direct CSS selector (e.g., "input[name='email']")
        else:
            raise ValueError("Invalid selector type. Use 'class', 'id', or 'css'.")

        await page.waitForSelector(selector, timeout=5000)  # Ensure element is loaded

        click_selector(page, element_type, element_value)
        clear_the_existing_data()
        await page.type(selector, text)  # Type the text
        print(f"Typed text into element: {selector}")
        return True
    except Exception as e:
        print(f"Error typing text ({element_type}: {element_value}): {e}")
        return False
