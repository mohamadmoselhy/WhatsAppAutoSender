import pywhatkit as kit
import pyautogui
import time
import ctypes  # For popup message
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileAddedHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:  # Ignore folder creation events
            file_path = event.src_path
            print(f"New file added: {file_path}")
            
            # Ask user for confirmation
            if self.confirm_send_file(file_path):  
                self.notify_user()  # ✅ Notify user to open WhatsApp
                self.send_file_via_whatsapp(file_path)  # ✅ Send file via WhatsApp
            else:
                print("❌ File sending canceled by user.")

    def confirm_send_file(self, file_path):
        """ Ask the user for confirmation before sending the file. """
        response = ctypes.windll.user32.MessageBoxW(
            0, f"Do you want to send this file?\n\n{file_path}", 
            "Confirm File Sending", 4  # 4 = Yes/No dialog
        )
        return response == 6  # Yes = 6, No = 7

    def notify_user(self):
        """ Display a popup message to the user to ensure WhatsApp Web is open. """
        ctypes.windll.user32.MessageBoxW(0, "Please open WhatsApp Web and ensure the chat is visible before proceeding.", "WhatsApp File Sender", 1)

    def send_file_via_whatsapp(self, file_path):
        try:
            contact_name = "vodafone Number"  # Change to recipient's name
            message = "مرحبا"
            
            # Step 1: Open WhatsApp Web
            pyautogui.hotkey("ctrl", "alt", "w")  # Opens WhatsApp Web (if shortcut exists)
            time.sleep(5)  # Wait for it to open
            
            # Step 2: Search for the contact
            NameField_icon = r"D:\My drive\Course\Data Science\Projects\Mostql\NameField.PNG"
            Name_location = pyautogui.locateCenterOnScreen(NameField_icon, confidence=0.8)
            if Name_location:
                pyautogui.click(Name_location)
                time.sleep(2)
            else:
                print("❌ Name field not found!")
                return

            pyautogui.write(contact_name)
            time.sleep(2)
            pyautogui.press("enter")  # Selects the contact
            time.sleep(2)
            
            # Step 3: Send the message
            pyautogui.write(message)
            pyautogui.press("enter")
            time.sleep(2)
            
            # Step 4: Locate and click the attachment button dynamically
            attachment_icon = r"D:\My drive\Course\Data Science\Projects\Mostql\Click.png"
            location = pyautogui.locateCenterOnScreen(attachment_icon, confidence=0.8)
            if location:
                pyautogui.click(location)
                time.sleep(2)
            else:
                print("❌ Attachment button not found!")
                return
            
            # Step 5: Click "Documents"
            document_icon = r"D:\My drive\Course\Data Science\Projects\Mostql\Document.png"
            doc_location = pyautogui.locateCenterOnScreen(document_icon, confidence=0.8)
            if doc_location:
                pyautogui.click(doc_location)
                time.sleep(2)
            else:
                print("❌ Document option not found!")
                return
            
            # Step 6: Type the file path and press Enter
            pyautogui.write(file_path)
            pyautogui.press("enter")
            time.sleep(2)
            
            # Step 7: Press "Enter" to send the file
            pyautogui.press("enter")
            print("✅ File sent successfully!")
        except Exception as e:
            print(f"❌ Error sending file: {e}")

# Monitor a folder for new files
folder_to_watch = r"D:\My drive\Course\Data Science\Projects\Mostql\Test Folder"

event_handler = FileAddedHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_watch, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)  # Keeps the script running
except KeyboardInterrupt:
    observer.stop()
observer.join()
