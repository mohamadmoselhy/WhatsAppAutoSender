# Core Module API Reference

## Configuration (`config.py`)

### `Config` Class
```python
class Config:
    def __init__(self):
        """Initialize configuration with environment variables"""
    
    def validate_paths(self):
        """Validate all configured paths"""
    
    def update_folder_path(self, new_path):
        """Update the folder path to monitor"""
```

## Logging (`logger.py`)

### `Logger` Class
```python
class Logger:
    def __init__(self):
        """Initialize logger with file and console handlers"""
    
    def debug(self, message):
        """Log debug message"""
    
    def info(self, message):
        """Log info message"""
    
    def warning(self, message):
        """Log warning message"""
    
    def error(self, message):
        """Log error message"""
    
    def critical(self, message):
        """Log critical message"""
    
    def exception(self, message):
        """Log exception with traceback"""
    
    def log_performance(self, operation, start_time):
        """Log performance metrics"""
```

## File Watching (`file_watcher.py`)

### `FileWatcher` Class
```python
class FileWatcher:
    def __init__(self, path, callback):
        """Initialize file watcher for given path"""
    
    def start(self):
        """Start watching for file changes"""
    
    def stop(self):
        """Stop watching for file changes"""
```

## Screenshot Utilities (`screenshot_utils.py`)

### Functions
```python
def capture_screenshot(filename):
    """Capture and save screenshot"""
    
def capture_error_screenshot():
    """Capture screenshot for error reporting"""
```

## Constants (`constants.py`)

### Configuration Constants
```python
DEFAULT_TEMP_MESSAGE_PATH = "src/MessageTemplates/NotificationToGroup.txt"
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
``` 