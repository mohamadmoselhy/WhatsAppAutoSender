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
        """Notify contact about files being ready"""
        try:
            # Get contact name and full relative folder path from file path
            contact_name, folder_name = self._get_contact_name_and_relative_folder(file_path)
            
            # Get all files in the same parent folder
            parent_folder = Path(file_path).parent
            files = []
            for pattern in config.file_patterns:
                files.extend(parent_folder.glob(pattern))
            
            # Prepare message
            Folder_Name_Encoded = urllib.parse.quote(contact_name)
            full_sharepoint_path = config.root_path + "/" + Folder_Name_Encoded

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
                    
                    # Format the message with bold and underline
                    formatted_message = message_content.replace('{memo_date}', f"*{hijri_date.day}/{hijri_date.month}/{hijri_date.year}*") \
                                                    .replace('{memo_gregorian_date}', f"*{today_gregorian.strftime('%d/%m/%Y')}*") \
                                                    .replace('{folder_name}', f"*_{folder_name}_*") \
                                                    .replace('{memo_link}', f"*{full_sharepoint_path}*") \
                                                    .replace('{file_name}', f"*{', '.join(f.name for f in files)}*")

                    # Update the message with the content
                    message = f"{formatted_message}"

            # Send notification
            return self.send_message_to_contact(contact_name, message)

        except Exception as e:
            logger.log_error(e, f"Failed to notify about files in {file_path}")
            self.whatsapp.close_application()
            raise

    def _get_contact_name_and_relative_folder(self, file_path: str) -> tuple:
        """
        Extract contact name and full relative folder path from file path
        Returns tuple of (contact_name, relative_folder_path)
        """
        try:
            path = Path(file_path)
            abs_path = path.absolute()
            # Find the contact name (folder after منظورة تجربة)
            parts = abs_path.parts
            try:
                index = parts.index("منظورة تجربة")
                if index + 1 < len(parts):
                    contact_name = parts[index + 1]
                else:
                    raise Exception(f"No folder found after 'منظورة تجربة' in path: {file_path}")
            except ValueError:
                raise Exception(f"Could not find 'منظورة تجربة' in path: {file_path}")
            # Get the full relative folder path from the main watch folder
            main_folder = Path(config.folder_to_watch)
            try:
                relative_folder = str(path.parent.relative_to(main_folder))
            except Exception:
                # fallback to just the parent folder name if relative fails
                relative_folder = path.parent.name
            logger.log_info(f"Contact name: {contact_name}, Relative folder: {relative_folder} from path: {file_path}")
            return contact_name, relative_folder
        except Exception as e:
            logger.log_error(e, f"Error extracting names from file path: {file_path}")
            raise

# Create global sender instance
sender = WhatsAppSender()

def send_file_via_whatsapp(file_path: str) -> bool:
    """Wrapper function for backward compatibility"""
    return sender.notify_file_ready(file_path) 