"""
WhatsApp utility functions for automation
"""

import time
import pyautogui
import pyperclip
from typing import Optional, Tuple
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from src.core.config import config
from src.core.logger import logger

def ask_user_to_send_message() -> bool:
    """
    Ask the user to send a message via WhatsApp Web
    Returns True if the user confirms, False otherwise
    """
    try:
        logger.log_info("Waiting for user to send message...")
        time.sleep(config.wait_time)
        return True
    except Exception as e:
        logger.log_error(e, "Error in ask_user_to_send_message")
        raise

def take_screenshot(error: Optional[Exception] = None) -> str:
    """
    Take a screenshot and save it to the logs directory
    Returns the path to the saved screenshot
    """
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"screenshot-{timestamp}.png"
        screenshot_path = os.path.join(config.log_dir, filename)
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        
        if error:
            logger.log_error(error, f"Screenshot saved to {screenshot_path}")
        else:
            logger.log_info(f"Screenshot saved to {screenshot_path}")
            
        return screenshot_path
    except Exception as e:
        logger.log_error(e, "Failed to take screenshot")
        raise

def wait_for_qr_scan() -> bool:
    """
    Wait for user to scan QR code and WhatsApp to load
    
    Returns:
        bool: True if WhatsApp loaded successfully, False otherwise
    """
    try:
        # Wait for WhatsApp to load (either QR code or chat list)
        logger.log_info("Waiting for WhatsApp to load...")
        
        # Try different selectors for QR code
        qr_selectors = [
            "div[data-testid='qrcode']",
            "div[data-ref]",
            "canvas[aria-label='Scan me!']"
        ]
        
        qr_code = None
        for selector in qr_selectors:
            try:
                qr_code = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if qr_code:
                    break
            except TimeoutException:
                raise
        
        if qr_code:
            logger.log_info("Please scan the QR code to login to WhatsApp Web")
            
            # Wait for QR code to disappear (indicating successful login)
            WebDriverWait(driver, 300).until_not(  # 5 minutes timeout for scanning
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-ref]"))
            )
        else:
            # If no QR code found, check if already logged in
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='chat-list']"))
                )
                logger.log_info("Already logged in to WhatsApp Web")
                return True
            except TimeoutException:
                logger.log_error(None, "Could not find QR code or chat list")
                raise
        
        # Wait for chat list to appear
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='chat-list']"))
        )
        
        logger.log_info("Successfully logged in to WhatsApp Web")
        return True
        
    except TimeoutException:
        logger.log_error(None, "QR code scan timed out")
        raise
    except Exception as e:
        logger.log_error(e, "Error during QR code scan")
        raise

def wait_for_element(selector: str, timeout: Optional[int] = None) -> bool:
    """
    Wait for an element to be present on the page
    
    Args:
        selector: CSS selector for the element
        timeout: Optional timeout in seconds
        
    Returns:
        bool: True if element was found, False otherwise
    """
    try:
        WebDriverWait(driver, timeout or config.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return True
    except TimeoutException:
        raise Exception(f"Timeout waiting for element: {selector}")

def click_element(image_path: str, timeout: int = 10) -> bool:
    """
    Click on an element when it appears
    Returns True if clicked, False if timeout
    """
    try:
        if wait_for_element(image_path, timeout):
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)
            if location:
                center = pyautogui.center(location)
                pyautogui.click(center)
                return True
        raise Exception(f"Could not find or click element: {image_path}")
    except Exception as e:
        logger.log_error(e, f"Error clicking element: {image_path}")
        raise

def type_message(message: str) -> bool:
    """
    Type a message in the WhatsApp Web input field
    Returns True if successful, False otherwise
    """
    try:
        pyautogui.write(message)
        return True
    except Exception as e:
        logger.log_error(e, "Error typing message")
        raise

def press_enter() -> bool:
    """
    Press the Enter key
    Returns True if successful, False otherwise
    """
    try:
        pyautogui.press('enter')
        return True
    except Exception as e:
        logger.log_error(e, "Error pressing Enter")
        raise

def get_user_choice() -> bool:
    """
    Ask the user to confirm sending the file
    Returns True if user confirms, False otherwise
    """
    try:
        logger.log_info("Waiting for user confirmation...")
        time.sleep(config.wait_time)
        return True
    except Exception as e:
        logger.log_error(e, "Error in get_user_choice")
        raise

def send_file(file_path: str) -> bool:
    """
    Send a file via WhatsApp Web
    Returns True if successful, False otherwise
    """
    try:
        # Click on the attachment button
        if not click_element(config.attachment_button_image):
            raise Exception("Could not find attachment button")

        # Click on the document option
        if not click_element(config.document_button_image):
            raise Exception("Could not find document button")

        # Type the file path and press enter
        pyautogui.write(file_path)
        pyautogui.press('enter')

        return True
    except Exception as e:
        logger.log_error(e, "Error sending file")
        raise

def write_in_field(text: str) -> bool:
    """
    Write text in the input field
    Returns True if successful, False otherwise
    """
    try:
        pyautogui.write(text)
        return True
    except Exception as e:
        logger.log_error(e, "Error writing in field")
        raise

def locate_image(image_path: str, timeout: int = 10) -> Optional[Tuple[int, int, int, int]]:
    """
    Locate an image on screen
    Returns the coordinates if found, None otherwise
    """
    try:
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateOnScreen(image_path, confidence=0.8)
                if location:
                    return location
            except pyautogui.ImageNotFoundException:
                pass
            time.sleep(0.5)
        raise Exception(f"Timeout locating image: {image_path}")
    except Exception as e:
        logger.log_error(e, f"Error locating image: {image_path}")
        raise

def clear_the_existing_data() -> bool:
    """
    Clear the input field
    Returns True if successful, False otherwise
    """
    try:
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        return True
    except Exception as e:
        logger.log_error(e, "Error clearing data")
        raise

def open_whatsapp_chat(contact_name: str) -> bool:
    """
    Open a chat with the specified contact
    Returns True if successful, False otherwise
    """
    try:
        # Find and click the search box
        if not click_element(config.search_box_image):
            raise Exception("Could not find search box")

        # Type the contact name
        if not write_in_field(contact_name):
            raise Exception("Could not type contact name")

        # Wait for the contact to appear and click it
        if not click_element(config.contact_image):
            raise Exception("Could not find contact")

        return True
    except Exception as e:
        logger.log_error(e, f"Error opening chat with {contact_name}")
        raise

def attach_file(file_path: str) -> bool:
    """
    Attach a file to the current chat
    Returns True if successful, False otherwise
    """
    try:
        # Click on the attachment button
        if not click_element(config.attachment_button_image):
            raise Exception("Could not find attachment button")

        # Click on the document option
        if not click_element(config.document_button_image):
            raise Exception("Could not find document button")

        # Type the file path and press enter
        pyautogui.write(file_path)
        pyautogui.press('enter')

        return True
    except Exception as e:
        logger.log_error(e, f"Error attaching file: {file_path}")
        raise

def send_message(message: str) -> bool:
    """
    Send a message in the current chat
    Returns True if successful, False otherwise
    """
    try:
        # Type the message
        if not write_in_field(message):
            raise Exception("Could not type message")

        # Press enter to send
        if not press_enter():
            raise Exception("Could not send message")

        return True
    except Exception as e:
        logger.log_error(e, "Error sending message")
        raise

def close_whatsapp_tab() -> bool:
    """
    Close the WhatsApp Web tab
    Returns True if successful, False otherwise
    """
    try:
        pyautogui.hotkey('ctrl', 'w')
        return True
    except Exception as e:
        logger.log_error(e, "Error closing WhatsApp tab")
        raise

# Global driver instance
driver: Optional[webdriver.Chrome] = None

def initialize_driver() -> bool:
    """
    Initialize the Selenium WebDriver
    Returns True if successful, False otherwise
    """
    try:
        global driver
        driver = webdriver.Chrome()
        driver.get("https://web.whatsapp.com")
        return True
    except Exception as e:
        logger.log_error(e, "Error initializing WebDriver")
        raise

def close_driver() -> None:
    """
    Close the Selenium WebDriver
    """
    try:
        if driver:
            driver.quit()
    except Exception as e:
        logger.log_error(e, "Error closing WebDriver")
        raise 