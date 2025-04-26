"""
WhatsApp message sender
"""

from pathlib import Path
from src.core.config import config
from src.core.logger import logger
from src.whatsapp.desktop_utils import WhatsAppDesktop
import urllib.parse
from datetime import datetime
from hijri_converter import convert
import os

class WhatsAppSender:
    def __init__(self):
        self.whatsapp = WhatsAppDesktop()

    def send_message_to_contact(self, contact_name: str, message: str) -> bool:
        """Send a message to a contact via WhatsApp"""
        try:
            # Connect to WhatsApp
            if not self.whatsapp.connect():
                return False

            # Open chat
            if not self.whatsapp.open_chat(contact_name):
                self.whatsapp.close_application()
                return False

            # Send message
            if not self.whatsapp.send_message(message):
                self.whatsapp.close_application()
                return False

            logger.log_info(f"Successfully sent message to {contact_name}")
            
            # Close WhatsApp after sending
            self.whatsapp.close_application()
            return True

        except Exception as e:
            logger.log_error(e, f"Failed to send message to {contact_name}")
            self.whatsapp.close_application()
            raise 

    def notify_file_ready(self, file_path: str) -> bool:
        """Notify contact about a file being ready"""
        try:
            # Get contact name from file path
            contact_name = self._get_contact_name(file_path)

            # Prepare message
            Folder_Name_Encoded = urllib.parse.quote(contact_name)
            full_sharepoint_path = config.root_path + "/" + Folder_Name_Encoded
            #message = f"New file is ready: {full_sharepoint_path}"

            if config.TempMessageForGroupPath:
                logger.log_info(f"Using custom message template from {os.path.abspath(config.TempMessageForGroupPath)}")
                with open(os.path.abspath(config.TempMessageForGroupPath), 'r', encoding='utf-8') as file:
                    # Read file content
                    lines = file.readlines()
                    
                    # Join the lines into a single string
                    message_content = ''.join(lines)
                    
                    # Get today's Gregorian date
                    today_gregorian = datetime.today()
                    
                    # Replace placeholders with actual values
                    hijri_date = convert.Gregorian(today_gregorian.year, today_gregorian.month, today_gregorian.day).to_hijri()
                    message_content = message_content.replace('{company_name}', contact_name) \
                                                   .replace('{memo_date}', f"{hijri_date.day}/{hijri_date.month}/{hijri_date.year}") \
                                                   .replace('{memo_gregorian_date}', today_gregorian.strftime('%d/%m/%Y')) \
                                                   .replace('{memo_link}', full_sharepoint_path)

                    # Update the message with the first line of the content
                    message = f"{message_content}"

            # Send notification
            return self.send_message_to_contact(contact_name, message)

        except Exception as e:
            logger.log_error(e, f"Failed to notify about file {file_path}")
            self.whatsapp.close_application()
            raise

    def _get_contact_name(self, file_path: str) -> str:
        """Extract contact name from file path"""
        try:
            path = Path(file_path)
            
            # Case 1: File is in a contact-named folder
            if path.parent.name != config.folder_to_watch:
                return path.parent.name
                
            # Case 2: File name contains contact name
            if "_" in path.stem:
                return path.stem.split("_")[0]
                
            # Case 3: Use default contact
            return False
            
        except Exception:
            raise

# Create global sender instance
sender = WhatsAppSender()

def send_file_via_whatsapp(file_path: str) -> bool:
    """Wrapper function for backward compatibility"""
    return sender.notify_file_ready(file_path) 