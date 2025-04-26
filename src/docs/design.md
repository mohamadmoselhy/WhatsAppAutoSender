# WhatsApp Auto Sender - Design Document

## Overview
The WhatsApp Auto Sender is a desktop application that monitors a specified folder for new files and automatically sends them via WhatsApp Desktop to predefined contacts.

## Architecture

### Core Components

1. **File Watcher**
   - Monitors specified folder for new files
   - Filters files based on extension and readiness
   - Triggers file processing when new files are detected
   - Handles file locking and temporary files

2. **WhatsApp Desktop Automation**
   - Connects to WhatsApp Desktop application
   - Manages window interaction and focus
   - Handles contact search and chat opening
   - Manages file attachment and sending
   - Handles message sending

3. **GUI Interface**
   - Provides status monitoring
   - Shows activity logs
   - Controls for starting/stopping monitoring
   - Error display and user feedback

4. **Configuration Management**
   - Manages application settings
   - Handles default contact names
   - Stores folder paths and other preferences

## Component Details

### File Watcher (`src/core/file_watcher.py`)
```python
class FileWatcher:
    def __init__(self, folder_path: str, callback: Callable[[str], None])
    def start() -> None
    def stop() -> None
    def is_file_ready(file_path: str) -> bool
    def should_process_file(file_path: str) -> bool
```

### WhatsApp Desktop Automation (`src/whatsapp/desktop_utils.py`)
```python
class WhatsAppDesktop:
    def __init__(self)
    def connect() -> bool
    def open_chat(contact_name: str) -> bool
    def attach_file(file_path: str) -> bool
    def send_message(message: str) -> bool
```

### GUI Interface (`src/gui/main_window.py`)
```python
class MainWindow:
    def __init__(self, root)
    def create_widgets()
    def update_status(message: str)
    def process_file(file_path: str)
    def start_monitoring()
    def stop_monitoring()
```

### Configuration (`src/core/config.py`)
```python
class Config:
    def __init__(self)
    def load_config() -> None
    def save_config() -> None
```

## Workflow

1. **Initialization**
   - Load configuration
   - Initialize WhatsApp Desktop connection
   - Set up file watcher
   - Create GUI interface

2. **Monitoring Process**
   - User clicks "Start Monitoring"
   - File watcher begins monitoring specified folder
   - When new file detected:
     - Check if file is ready for processing
     - Extract contact name from file path
     - Open WhatsApp chat with contact
     - Attach and send file
     - Log success/failure

3. **Error Handling**
   - Log all errors to activity log
   - Show error messages in GUI
   - Handle WhatsApp connection issues
   - Handle file processing failures

## File Structure
```
src/
├── core/
│   ├── config.py
│   ├── file_watcher.py
│   └── logger.py
├── gui/
│   └── main_window.py
├── whatsapp/
│   ├── desktop_utils.py
│   └── sender.py
└── main.py
```

## Configuration
The application uses a YAML configuration file (`config.yaml`) with the following settings:
- `folder_to_watch`: Path to monitor for files
- `default_contact`: Default contact name if not specified in file path
- `message`: Optional message to send with files
- `retry_attempts`: Number of retries for failed operations
- `retry_delay`: Delay between retry attempts
- `timeout`: Operation timeout in seconds

## Error Handling
- All operations are wrapped in try-except blocks
- Errors are logged to both console and GUI
- Failed operations are retried based on configuration
- Critical errors are displayed to user

## Security Considerations
- No sensitive data storage
- WhatsApp session management handled by WhatsApp Desktop
- File paths sanitized before use
- No network communication outside WhatsApp

## Future Enhancements
1. Support for multiple contacts per file
2. File type validation and conversion
3. Scheduled sending
4. Contact management interface
5. Batch processing capabilities
6. Progress tracking for large files
7. Custom message templates
8. File organization after sending 