import os

# Path to your batch file
config_file_path = "C:\Program Files\FolderListner\Config.txt"

# Dictionary to store key-value pairs
config = {}

# Read the text file and parse variables
with open(config_file_path, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if "=" in line:  # Ensure it follows the key=value format
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()


folder_to_watch=config.get("folder_to_watch")
contact_name=config.get("contact_name")
message=config.get("message")
name_field=config.get("name_field")
name_field2=config.get("name_field2")
attachment=config.get("attachment")
document=config.get("document")
whatsapp_images=config.get("whatsapp_images")
message_box=config.get("message_box")


