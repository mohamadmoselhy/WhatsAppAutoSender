# Configuration Guide

## Environment Variables

The application uses the following environment variables:

```env
WHATSAPP_GROUP_NAME=Your Group Name
MESSAGE_INTERVAL=300
FOLDER_TO_WATCH=C:\Path\To\Watch
APP_VERSION=1.0
DEVELOPER=Mohamed Moselhy
SUPPORT_EMAIL=Mohamed_Moselhy@outlook.com
```

## Configuration Options

### WhatsApp Group
- Name of the target WhatsApp group
- Must match exactly as shown in WhatsApp Desktop

### Message Interval
- Time between checks for new files
- Range: 60-3600 seconds
- Default: 300 seconds (5 minutes)

### Folder to Watch
- Directory to monitor for file changes
- Can be created during installation
- Must have read permissions

## Message Templates

Templates are stored in `MessageTemplates/`:
- `NotificationToGroup.txt`: Default message template
- Supports variables: `{filename}`, `{timestamp}`, etc.

## Logging Configuration

Log files:
- Location: `logs/whatsapp_auto_sender_YYYYMMDD.log`
- Rotation: 5MB per file
- Backups: 5 files maintained
- Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

## Troubleshooting

Common configuration issues:
1. WhatsApp group name mismatch
2. Insufficient folder permissions
3. Invalid message interval
4. Template file not found 