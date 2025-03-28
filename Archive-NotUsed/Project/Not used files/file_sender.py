import pyautogui
import pyperclip
from whatsapp_utils import locate_image
from config import icons

def send_file(file_path):
    """Attaches and sends the file via WhatsApp."""
    print(f"[INFO] Attempting to send file: {file_path}")
    
    attachment_location = locate_image(icons["attachment"])
    if attachment_location:
        pyautogui.click(attachment_location)
        time.sleep(2)
        print("[INFO] Clicked attachment button.")
    else:
        print("❌ Attachment button not found!")
        return

    doc_location = locate_image(icons["document"])
    if doc_location:
        pyautogui.click(doc_location)
        time.sleep(2)
        print("[INFO] Clicked document option.")
    else:
        print("❌ Document option not found!")
        return

    time.sleep(2)
    print(f"[INFO] Pasting file path: {file_path}")
    pyperclip.copy(file_path)  # Copy Arabic file path to clipboard
    pyautogui.hotkey("ctrl", "v")  # Paste the file path
    time.sleep(1)
    pyautogui.press("enter")  # Confirm file selection
    time.sleep(3)
    pyautogui.press("enter")  # Send file
    print(f"✅ File '{file_path}' sent successfully!")
