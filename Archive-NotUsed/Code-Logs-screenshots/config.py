import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to your batch file
config_file_path = r"C:\Program Files\FolderListner\Config.txt"  # Use raw string to avoid escape issues

# Dictionary to store key-value pairs
config = {}

# Log the start of configuration file reading
logging.info("Starting to read configuration from file: %s", config_file_path)

try:
    with open(config_file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "=" in line:  # Ensure it follows the key=value format
                try:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
                    logging.info("Loaded configuration: %s = %s", key.strip(), value.strip())
                except ValueError as e:
                    logging.warning("Skipping invalid line: '%s'. Error: %s", line, e)
            else:
                logging.warning("Skipping invalid format (missing '=' in line): '%s'", line)

    # Log successful reading of the file
    logging.info("Configuration file loaded successfully.")

except FileNotFoundError:
    logging.error("Configuration file not found at: %s", config_file_path)
except Exception as e:
    logging.error("Error reading the configuration file: %s", e)

# Retrieve configuration values
folder_to_watch = config.get("folder_to_watch", "DefaultFolderPath")
contact_name = config.get("contact_name", "Default Contact Name")
message = config.get("message", "Default message")
name_field = config.get("name_field", "Default Name Field")
name_field2 = config.get("name_field2", "Default Name Field 2")
attachment = config.get("attachment", "Default Attachment Path")
document = config.get("document", "Default Document Path")
whatsapp_images = config.get("whatsapp_images", "Default Image Path")
message_box = config.get("message_box", "Default Message Box")

# Log the retrieved configuration values
logging.info("Configuration values loaded:")
logging.info("Folder to Watch: %s", folder_to_watch)
logging.info("Contact Name: %s", contact_name)
logging.info("Message: %s", message)
logging.info("Name Field: %s", name_field)
logging.info("Name Field 2: %s", name_field2)
logging.info("Attachment: %s", attachment)
logging.info("Document: %s", document)
logging.info("WhatsApp Images: %s", whatsapp_images)
logging.info("Message Box: %s", message_box)
