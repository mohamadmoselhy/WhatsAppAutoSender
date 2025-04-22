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

from src.core.logger import logger

class WhatsAppDesktop:
    def __init__(self):
        self.app = None
        self.main_window = None
        # Microsoft Store WhatsApp package name
        self.whatsapp_app_id = "5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"

    def connect(self) -> bool:
        """Connect to WhatsApp desktop application or launch it if not running"""
        try:
            # Try to find existing WhatsApp window
            try:
                self.app = Application(backend="uia").connect(title="WhatsApp")
                self.main_window = self.app.window(title="WhatsApp")
                logger.log_info("Connected to existing WhatsApp instance")
                return True
            except Exception:
                logger.log_info("WhatsApp is not running. Launching application...")
                
                try:
                    # Launch WhatsApp using shell execute
                    subprocess.Popen([
                        "explorer.exe", 
                        f"shell:AppsFolder\\{self.whatsapp_app_id}"
                    ])
                except Exception as e:
                    logger.log_error(e, "Failed to launch WhatsApp. Make sure it's installed from Microsoft Store.")
                    return False
                
                # Wait for the window to appear (up to 30 seconds)
                wait_time = 30
                start_time = time.time()
                while time.time() - start_time < wait_time:
                    try:
                        self.app = Application(backend="uia").connect(title="WhatsApp")
                        self.main_window = self.app.window(title="WhatsApp")
                        logger.log_info("Connected to WhatsApp desktop")
                        return True
                    except Exception:
                        time.sleep(1)
                        continue
                
                logger.log_error(None, "WhatsApp failed to start")
                return False
            
        except Exception as e:
            logger.log_error(e, "Failed to connect to WhatsApp desktop")
            return False

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
            return False

    def open_chat(self, contact_name: str) -> bool:
        """Open a chat with the specified contact"""
        try:
            if not self.main_window:
                logger.log_error(None, "WhatsApp window not connected")
                return False

            # Find the search box using exact UiPath properties
            search_box = self.main_window.child_window(
                auto_id="SearchQueryTextBox",
                class_name="TextBox"
            )
            
            if not search_box.exists():
                logger.log_error(None, "Could not find search box")
                return False
            
            # Focus and clear the search box
            search_box.set_focus()
            time.sleep(0.5)
            
            search_box.type_keys('^a{BACKSPACE}')
            time.sleep(0.5)
            
            # Type the contact name
            search_box.type_keys(contact_name, with_spaces=True)
            time.sleep(2)  # Wait for search results
            
            try:
                # Find the ChatList first
                chat_list = self.main_window.child_window(
                    auto_id="ChatList",
                    class_name="ListView",
                    title="Chats list"
                )
                
                if not chat_list.exists():
                    logger.log_error(None, "Could not find chat list")
                    return False

                # Find the contact using TextBlock with wildcard name matching
                contact_element = chat_list.child_window(
                    auto_id="Title",
                    class_name="TextBlock",
                    title_re=f".*{contact_name}.*"
                )

                if contact_element.exists() and contact_element.is_visible():
                    # Click the parent ListItem
                    parent = contact_element.parent()
                    if parent and parent.element_info.control_type == "ListItem":
                        parent.click_input()
                        time.sleep(2)  # Wait for chat to open
                        return True
                    else:
                        # If parent check fails, try clicking the contact element directly
                        contact_element.click_input()
                        time.sleep(2)
                        return True
                
                logger.log_error(None, f"Could not find contact: {contact_name}")
                return False
                
            except Exception as e:
                logger.log_error(e, f"Failed to find and click contact: {contact_name}")
                return False
            
        except Exception as e:
            logger.log_error(e, f"Failed to open chat with {contact_name}")
            return False

    def send_message(self, message: str) -> bool:
        """Send a message in the current chat"""
        try:
            if not self.main_window:
                logger.log_error(None, "WhatsApp window not connected")
                return False

            # Find the message input box using exact UiPath properties
            message_box = self.main_window.child_window(
                auto_id="InputBarTextBox",
                class_name="RichEditBox"
            )
            
            if not message_box.exists():
                logger.log_error(None, "Could not find message input box")
                return False
                
            # Type message
            message_box.set_focus()
            time.sleep(0.5)
            
            message_box.type_keys('^a{BACKSPACE}')  # Clear existing text
            time.sleep(0.5)
            
            message_box.type_keys(message, with_spaces=True)
            time.sleep(0.5)
            
            # Find and click the send button
            send_button = self.main_window.child_window(
                auto_id="RightButton",
                class_name="Button"
            )
            
            if not send_button.exists():
                logger.log_error(None, "Could not find send button")
                return False
                
            send_button.click_input()
            time.sleep(1)
            
            return True
            
        except Exception as e:
            logger.log_error(e, "Failed to send message")
            return False 