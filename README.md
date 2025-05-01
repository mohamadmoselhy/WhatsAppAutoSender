# WhatsApp Auto Sender

An automated solution for sending WhatsApp messages based on file system changes.

## Features

- Automatically send WhatsApp messages to specified groups
- Monitor folders for file changes
- Customizable message templates
- Easy-to-use installer
- Configurable message intervals
- Automatic startup option

## System Requirements

- Windows 10 or later (64-bit)
- WhatsApp Desktop application installed and logged in
- Minimum 4GB RAM
- Stable internet connection

## Installation

1. Download `WhatsAppAutoSender-Setup.exe`
2. Run the installer as administrator
3. Follow the installation wizard:
   - Accept the license agreement
   - Choose installation directory
   - Configure WhatsApp group name
   - Set message check interval (60-3600 seconds)
   - Select folder to monitor
   - Choose startup options

## Configuration

The application can be configured through:
1. Installation wizard
2. `.env` file in the installation directory
3. Settings menu in the application

### Environment Variables
- `WHATSAPP_GROUP_NAME`: Target WhatsApp group
- `MESSAGE_INTERVAL`: Check interval in seconds
- `FOLDER_TO_WATCH`: Directory to monitor for changes

## Usage

1. Ensure WhatsApp Desktop is running and logged in
2. Launch WhatsApp Auto Sender
3. The application will:
   - Monitor the specified folder
   - Send messages according to the template
   - Create logs in the logs directory

## Support

For support, please contact:
- Email: Mohamed_Moselhy@outlook.com

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Developer

Mohamed Moselhy
- Email: Mohamed_Moselhy@outlook.com

---

© 2024 Mohamed Moselhy. All rights reserved. 