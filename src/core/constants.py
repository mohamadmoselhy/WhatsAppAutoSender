"""
Core Module Constants
"""

# File System Constants
DEFAULT_FOLDER_TO_WATCH = r"C:\Users\Lenovo\OneDrive\قضايا التحكيم\منظورة تجربة"
DEFAULT_TEMP_MESSAGE_PATH = "src/MessageTemplates/NotificationToGroup.txt"
DEFAULT_ROOT_PATH = "	https://ta7kem-my.sharepoint.com/personal/contact_ta7kem_com/Documents/%D9%82%D8%B6%D8%A7%D9%8A%D8%A7%20%D8%A7%D9%84%D8%AA%D8%AD%D9%83%D9%8A%D9%85/%D9%85%D9%86%D8%B8%D9%88%D8%B1%D8%A9%20%D8%AA%D8%AC%D8%B1%D8%A8%D8%A9"

# Logging Constants
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_LEVEL = "INFO"
LOG_FILE = "whatsapp_auto_sender.log"

# File Watching Constants
FILE_CHECK_INTERVAL = 1  # seconds
MAX_FILE_AGE = 300  # seconds (5 minutes)
FILE_PATTERNS = ["*.pdf", "*.doc", "*.docx", "*.xls", "*.xlsx"]

# Error Handling Constants
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
ERROR_WAIT_TIME = 10  # seconds

# Message Template Constants
MESSAGE_PLACEHOLDERS = {
    "company_name": "{company_name}",
    "memo_date": "{memo_date}",
    "memo_gregorian_date": "{memo_gregorian_date}",
    "memo_link": "{memo_link}",
    "file_name": "{file_name}",
    "folder_name": "{folder_name}"
} 