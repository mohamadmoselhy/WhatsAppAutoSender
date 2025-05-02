"""
WhatsApp desktop automation
"""

import time
import os
import subprocess
import re
from pywinauto.application import Application
from pywinauto.findwindows import find_windows
from pywinauto.keyboard import send_keys
from pywinauto.timings import wait_until
import pyperclip
import time
from pywinauto.keyboard import send_keys

from src.core.logger import logger
from src.core.whatsapp_constants import *

class WhatsAppDesktop:
    def __init__(self):
        self.app = None
        self.main_window = None

    def connect(self) -> bool:
        """Connect to WhatsApp desktop application or launch it if not running"""
        try:
            logger.log_info("Attempting to connect to WhatsApp...")
            # Try to find existing WhatsApp window
            try:
                self.app = Application(backend="uia").connect(title=WHATSAPP_WINDOW_TITLE)
                self.main_window = self.app.window(title=WHATSAPP_WINDOW_TITLE)
                logger.log_info("Connected to existing WhatsApp instance")
                return True
            except Exception:
                logger.log_info("WhatsApp is not running. Launching application...")
                
                try:
                    # Launch WhatsApp using shell execute
                    logger.log_info(f"Launching WhatsApp with ID: {WHATSAPP_APP_ID}")
                    subprocess.Popen([
                        "explorer.exe", 
                        f"shell:AppsFolder\\{WHATSAPP_APP_ID}"
                    ])
                except Exception as e:
                    logger.log_error(e, "Failed to launch WhatsApp. Make sure it's installed from Microsoft Store.")
                    raise
                
                # Wait for the window to appear
                logger.log_info(f"Waiting up to {WAIT_TIME} seconds for WhatsApp to start...")
                start_time = time.time()
                while time.time() - start_time < WAIT_TIME:
                    try:
                        self.app = Application(backend="uia").connect(title=WHATSAPP_WINDOW_TITLE)
                        self.main_window = self.app.window(title=WHATSAPP_WINDOW_TITLE)
                        logger.log_info("Connected to WhatsApp desktop")
                        return True
                    except Exception:
                        time.sleep(1)
                        continue
                
                raise Exception("WhatsApp failed to start")
            
        except Exception as e:
            logger.log_error(e, "Failed to connect to WhatsApp desktop")
            raise

    def close_application(self) -> bool:
        """Close WhatsApp application"""
        try:
            # Use taskkill for both WhatsApp.exe and ApplicationFrameHost.exe
            try:
                subprocess.run(['taskkill', '/F', '/IM', 'ApplicationFrameHost.exe'],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
                time.sleep(1)
            except Exception:
                pass

            # Clear the references
            self.main_window = None
            self.app = None
            
            logger.log_info("WhatsApp closed successfully")
            return True

        except Exception as e:
            logger.log_error(e, "Failed to close WhatsApp")
            raise

    def open_chat(self, contact_name: str) -> bool:
        """Open a chat with the specified contact"""
        try:
            logger.log_info(f"Attempting to open chat with {contact_name}...")
            if not self.main_window:
                raise Exception("WhatsApp window not connected")

            # Find the search box
            logger.log_info("Looking for search box...")
            search_box = self.main_window.child_window(
                auto_id=SEARCH_BOX_AUTO_ID,
                class_name=SEARCH_BOX_CLASS
            )
            
            if not search_box.exists():
                raise Exception("Could not find search box")
            
            # Focus and clear the search box
            logger.log_info("Clearing search box...")
            search_box.set_focus()
            time.sleep(CLICK_DELAY)
            search_box.type_keys('^a{BACKSPACE}')
            time.sleep(CLICK_DELAY)
            
            # Type the contact name
            logger.log_info(f"Typing contact name: {contact_name}")
            search_box.type_keys(contact_name, with_spaces=True)
            time.sleep(SEARCH_DELAY)
            
            try:
                # Find the ChatList
                logger.log_info("Looking for chat list...")
                chat_list = self.main_window.child_window(
                    auto_id=CHAT_LIST_AUTO_ID,
                    class_name=CHAT_LIST_CLASS,
                    title=CHAT_LIST_TITLE
                )
                
                if not chat_list.exists():
                    raise Exception("Could not find chat list")

                # Find the contact
                logger.log_info(f"Searching for contact: {contact_name}")
                contact_element = chat_list.child_window(
                    auto_id=CONTACT_TITLE_AUTO_ID,
                    class_name=CONTACT_TITLE_CLASS,
                    title_re=f".*{contact_name}.*",
                    top_level_only=False,
                    found_index=0
                )

                if contact_element.exists() and contact_element.is_visible():
                    logger.log_info("Contact found, attempting to open chat...")
                    # Click the parent ListItem
                    parent = contact_element.parent()
                    if parent and parent.element_info.control_type == "ListItem":
                        parent.click_input()
                        time.sleep(CHAT_OPEN_DELAY)
                        logger.log_info("Chat opened successfully")
                        return True
                    else:
                        # If parent check fails, try clicking the contact element directly
                        contact_element.click_input()
                        time.sleep(CHAT_OPEN_DELAY)
                        logger.log_info("Chat opened successfully (direct click)")
                        return True
                
                raise Exception(f"Could not find contact: {contact_name}")
                
            except Exception as e:
                logger.log_error(e, f"Failed to find and click contact: {contact_name}")
                raise
            
        except Exception as e:
            logger.log_error(e, f"Failed to open chat with {contact_name}")
            raise

    def send_message(self, message: str) -> bool:
        """Send a message in the current chat"""
        try:
            logger.log_info("Preparing to send message...")
            if not self.main_window:
                raise Exception("WhatsApp window not connected")

            # Find the message input box
            logger.log_info("Looking for message input box...")
            message_box = self.main_window.child_window(
                auto_id=MESSAGE_BOX_AUTO_ID,
                class_name=MESSAGE_BOX_CLASS
            )
            
            if not message_box.exists():
                raise Exception("Could not find message input box")
                
            # Focus and clear existing text
            logger.log_info("Clearing message input box...")
            message_box.set_focus()
            time.sleep(CLICK_DELAY)
            message_box.type_keys('^a{BACKSPACE}')
            time.sleep(CLICK_DELAY)

            # Copy the message to clipboard
            logger.log_info("Copying message to clipboard...")
            pyperclip.copy(message)
            time.sleep(CLICK_DELAY)  # Wait for clipboard to be ready
            logger.log_info(f"Message copied to clipboard: {message}")

            # Paste the message
            logger.log_info("Pasting message...")
            message_box.click_input()
            time.sleep(CLICK_DELAY)
            send_keys('^v')
            time.sleep(CLICK_DELAY)
            
            
            # Find and click the send button
            logger.log_info("Looking for send button...")
            send_button = self.main_window.child_window(
                auto_id=SEND_BUTTON_AUTO_ID,
                class_name=SEND_BUTTON_CLASS
            )
            
            if not send_button.exists():
                raise Exception("Could not find send button")
                
            logger.log_info("Clicking send button...")
            send_button.click_input()
            time.sleep(MESSAGE_SEND_DELAY)
            
            logger.log_info("Message sent successfully")
            return True
            
        except Exception as e:
            logger.log_error(e, "Failed to send message")
            raise
