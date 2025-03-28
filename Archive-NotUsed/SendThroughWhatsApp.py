import pywhatkit as kit
import pyautogui
import time

# Step 1: Open WhatsApp Web and type the message
kit.sendwhatmsg_instantly("+201146845411", "Here is your file!")

# Step 2: Wait for the chat to open
time.sleep(10)

# Step 3: Locate and click the attachment button dynamically
attachment_icon = "D:\My drive\Course\Data Science\Projects\Mostql\Click.png"
location = pyautogui.locateCenterOnScreen(attachment_icon, confidence=0.8)  # Adjust confidence if needed

if location:
    pyautogui.click(location)
    time.sleep(2)
else:
    print("Attachment button not found!")

# Step 4: Click "Photos & Videos" or "Documents" dynamically
document_icon = "D:\My drive\Course\Data Science\Projects\Mostql\Document.png"  # Screenshot the document option
doc_location = pyautogui.locateCenterOnScreen(document_icon, confidence=0.8)

if doc_location:
    pyautogui.click(doc_location)
    time.sleep(2)
else:
    print("Document option not found!")

# Step 5: Type the file path and press Enter
file_path = r"D:\My drive\Course\Data Science\Projects\Mostql\Test Folder\New Rich Text Document.rtf"
pyautogui.write(file_path)
pyautogui.press("enter")
time.sleep(2)

# Step 6: Press "Enter" to send the file
pyautogui.press("enter")

print("File sent successfully!")
