# WhatsApp Auto Sender - Solution Manual

## Table of Contents
1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [Usage Guide](#usage-guide)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

## Introduction
WhatsApp Auto Sender is an automated messaging application designed to send messages to WhatsApp groups or contacts automatically. It uses the WhatsApp Desktop application to send messages and can be configured to send messages at specific times or in response to certain triggers.

## System Requirements
- Windows 10 or later
- WhatsApp Desktop application installed and logged in
- Minimum 4GB RAM
- Stable internet connection

## Installation Guide

1. Download the `WhatsAppAutoSender-Setup.exe` installer
2. Run the installer and follow these steps:
   - Accept the license agreement
   - Choose the installation directory (default is recommended)
   - Select the folder to monitor for new files
   - Choose whether to create a desktop shortcut
3. Click "Install" to complete the installation

The installer will:
- Install the application in the selected directory
- Create necessary folders and files
- Set up the folder to monitor
- Create a desktop shortcut (if selected)
- Add an uninstaller in Windows Programs and Features

## Configuration

### Folder Selection
During installation, you will be prompted to select a folder to monitor. This folder will be checked for new files that trigger message sending. You can change this folder later by:
1. Open the application
2. Go to Settings
3. Click "Change Folder"
4. Select the new folder to monitor

### Message Templates
1. Navigate to the installed application directory
2. Open the `MessageTemplates` folder
3. Edit `NotificationToGroup.txt` to customize your message template
4. Use placeholders like `{date}`, `{time}`, etc. for dynamic content

### Environment Variables
The installer creates a `.env` file with the following settings:
```
WHATSAPP_GROUP_NAME=Your Group Name
MESSAGE_INTERVAL=300  # Time between messages in seconds
FOLDER_TO_WATCH=path_to_your_selected_folder
```

You can edit these settings in the `.env` file located in the application directory.

## Usage Guide

### Starting the Application
1. Ensure WhatsApp Desktop is running and logged in
2. Launch `WhatsAppAutoSender.exe`
3. The application will automatically connect to WhatsApp Desktop

### Sending Messages
1. The application will monitor the configured folder for new files
2. When a new file is detected, it will:
   - Read the message template
   - Replace placeholders with current values
   - Send the message to the specified WhatsApp group

### Monitoring
- The application creates logs in the `logs` directory
- Check the logs for any errors or issues
- Log files are named with the format: `YYYYMMDD_whatsapp_auto_sender.log`

## Troubleshooting

### Common Issues

1. **Application not connecting to WhatsApp**
   - Ensure WhatsApp Desktop is running
   - Check if you're logged in to WhatsApp Desktop
   - Verify the group name in the configuration

2. **Messages not sending**
   - Check the logs for error messages
   - Verify the message template format
   - Ensure the group name is correct

3. **Permission Issues**
   - Run the application as administrator
   - Check if the application has write permissions to the log directory

### Error Messages

- **FileNotFoundError**: Template file not found
  - Solution: Ensure the MessageTemplates folder is in the same directory as the executable

- **ConnectionError**: Cannot connect to WhatsApp
  - Solution: Check WhatsApp Desktop status and internet connection

## FAQ

### Q: Can I send messages to multiple groups?
A: Currently, the application supports sending to one group at a time. You can change the group in the configuration.

### Q: How do I customize the message format?
A: Edit the `NotificationToGroup.txt` file in the MessageTemplates folder.

### Q: Can I schedule messages for specific times?
A: Yes, you can configure the message interval in the .env file.

### Q: Is there a limit to message length?
A: The application follows WhatsApp's message length limits.

### Q: How do I stop the application?
A: Close the application window or use Task Manager to end the process.

## Support
For additional support or questions, please contact the development team.

---

*Note: This documentation is subject to updates. Please check for the latest version.* 