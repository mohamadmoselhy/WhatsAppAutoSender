# Architecture Overview

## System Components

### Core Module
- `config.py`: Configuration management
- `logger.py`: Logging system
- `file_watcher.py`: File system monitoring
- `screenshot_utils.py`: Screenshot capture utilities
- `constants.py`: Application constants

### WhatsApp Module
- `desktop_utils.py`: WhatsApp Desktop automation
- `utils.py`: WhatsApp utility functions
- `sender.py`: Message sending functionality

## Data Flow

1. File System Monitoring
   - `file_watcher.py` monitors specified directory
   - Triggers events on file changes

2. Message Processing
   - Reads template from `MessageTemplates/`
   - Processes template with file information
   - Prepares message for sending

3. WhatsApp Integration
   - Uses `pywinauto` for desktop automation
   - Sends messages to specified group
   - Handles errors and retries

## Configuration

Configuration is managed through:
1. `.env` file
2. Installation wizard
3. Application settings

## Logging

Logs are stored in:
- `logs/whatsapp_auto_sender_YYYYMMDD.log`
- Rotating log files (5MB each)
- 5 backup files maintained 