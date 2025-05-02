# WhatsApp Module API Reference

## Desktop Utilities (`desktop_utils.py`)

### `WhatsAppDesktop` Class
```python
class WhatsAppDesktop:
    def __init__(self):
        """Initialize WhatsApp Desktop automation"""
    
    def connect(self):
        """Connect to WhatsApp Desktop"""
    
    def find_group(self, group_name):
        """Find and select WhatsApp group"""
    
    def send_message(self, message):
        """Send message to selected group"""
    
    def is_connected(self):
        """Check if connected to WhatsApp"""
```

## Utilities (`utils.py`)

### Functions
```python
def process_template(template_path, variables):
    """Process message template with variables"""
    
def validate_group_name(group_name):
    """Validate WhatsApp group name"""
    
def format_message(message, variables):
    """Format message with variables"""
```

## Sender (`sender.py`)

### `MessageSender` Class
```python
class MessageSender:
    def __init__(self):
        """Initialize message sender"""
    
    def send(self, message):
        """Send message to WhatsApp group"""
    
    def retry_send(self, message, max_retries=3):
        """Retry sending message on failure"""
    
    def validate_message(self, message):
        """Validate message before sending"""
```

## WhatsApp Constants (`whatsapp_constants.py`)

### Configuration Constants
```python
WHATSAPP_WINDOW_TITLE = "WhatsApp"
GROUP_SEARCH_TIMEOUT = 10
MESSAGE_SEND_TIMEOUT = 5
MAX_RETRIES = 3
RETRY_DELAY = 2
``` 