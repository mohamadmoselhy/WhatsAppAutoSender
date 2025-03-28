import time
import pyautogui
import pyperclip  # To handle Arabic text
from whatsapp_utils import locate_image
from config import message, icons

def send_message():
    """Sends only the message to the contact."""
    print("[INFO] Attempting to send message...")
    msg_box = locate_image(icons["message_box"])
    if msg_box:
        pyautogui.click(msg_box)
        time.sleep(1)
        print(f"[INFO] Pasting message: {message}")
        pyperclip.copy(message)  # Copy Arabic text to clipboard
        pyautogui.hotkey("ctrl", "v")  # Paste the message
        time.sleep(1)
        pyautogui.press("enter")  # Send the message
        time.sleep(2)
        print("✅ Message sent successfully!")
    else:
        print("❌ Message box not found!")
