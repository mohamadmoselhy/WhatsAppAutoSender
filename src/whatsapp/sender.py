"""
WhatsApp message sender
"""

from pathlib import Path
from src.core.config import config
from src.core.logger import logger
from src.whatsapp.desktop_utils import WhatsAppDesktop

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
            return False

    def notify_file_ready(self, file_path: str) -> bool:
        """Notify contact about a file being ready"""
        try:
            # Get contact name from file path
            contact_name = self._get_contact_name(file_path)

            # Prepare message
            root_path = "https://gizasystems-my.sharepoint.com/personal/mohamed_moselhy_gizasystems_com/Documents/%D9%82%D8%B6%D8%A7%D9%8A%D8%A7%20%D8%A7%D9%84%D8%AA%D8%AD%D9%83%D9%8A%D9%85/%D9%85%D9%86%D8%B8%D9%88%D8%B1%D8%A9%20%D8%AA%D8%AC%D8%B1%D8%A8%D8%A9"
            Folder_Name = "%D8%AA%D8%AC%D8%B1%D8%A8%D8%A9%201"
            full_sharepoint_path = root_path + "/" + Folder_Name
            message = f"New file is ready: {full_sharepoint_path}"
            if config.message:
                message = f"{config.message}\n{message}"

            # Send notification
            return self.send_message_to_contact(contact_name, message)

        except Exception as e:
            logger.log_error(e, f"Failed to notify about file {file_path}")
            self.whatsapp.close_application()
            return False

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
            return config.default_contact
            
        except Exception:
            return config.default_contact

# Create global sender instance
sender = WhatsAppSender()

def send_file_via_whatsapp(file_path: str) -> bool:
    """Wrapper function for backward compatibility"""
    return sender.notify_file_ready(file_path) 