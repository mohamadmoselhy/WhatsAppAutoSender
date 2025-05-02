
# WhatsApp Auto Sender - Solution Manual

## Table of Contents
1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [Usage Guide](#usage-guide)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)
8. [About the Developer](#about-the-developer)
9. [Support](#support)

## Introduction
WhatsApp Auto Sender is an automated messaging application designed to send messages to WhatsApp groups or contacts automatically. It uses the WhatsApp Desktop application to send messages and can be configured to send messages at specific times or in response to certain triggers.

## System Requirements
- Windows 10 or later  
- WhatsApp Desktop application installed and logged in  
- Minimum 4GB RAM  
- Stable internet connection  

## Installation Guide
1. Create a new folder for the application (e.g., `WhatsAppAutoSender`)  
2. Copy the following files to this folder:  
   - `WhatsAppAutoSender.exe`  
   - `MessageTemplates` folder  
   - `.env` file (if provided)  
3. Double-click `WhatsAppAutoSender.exe` to run the application  

## Configuration

### Message Templates
1. In your application folder, locate the `MessageTemplates` folder  
2. Edit `MessageTemplates/NotificationToGroup.txt` to customize your message template  
3. Use placeholders like `{date}`, `{time}`, etc. for dynamic content  

### Environment Variables
If you received a `.env` file:  
1. Place it in the same folder as `WhatsAppAutoSender.exe`  
2. Edit the following variables as needed:  
   ```
   WHATSAPP_GROUP_NAME=Your Group Name
   MESSAGE_INTERVAL=300  # Time between messages in seconds
   ```

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
  - *Solution:* Ensure the MessageTemplates folder is in the same directory as the executable  

- **ConnectionError**: Cannot connect to WhatsApp  
  - *Solution:* Check WhatsApp Desktop status and internet connection  

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

## About the Developer

This application was developed by **Mohamed Moselhy**, a Senior RPA Developer and Automation Specialist based in Cairo, Egypt. With a strong background in mechatronics and software automation, Mohamed has delivered multiple high-impact automation solutions using tools like UiPath, Power Automate, and custom-built utilities such as this WhatsApp Auto Sender. He is passionate about empowering users with smart tools that enhance productivity and efficiency.

- GitHub: [github.com/MohamedMoselhy](https://github.com/MohamedMoselhy)  
- LinkedIn: [linkedin.com/in/mohamedmoselhy](https://www.linkedin.com/in/mohamedmoselhy)  
- Email: mohamed.moselhy.dev@gmail.com  

## Support

For additional support or questions, please contact:

**Mohamed Moselhy**  
Senior RPA Developer  
📧 mohamed.moselhy.dev@gmail.com  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/mohamedmoselhy)  

---

*Note: This documentation is subject to updates. Please check for the latest version.*
