# WhatsApp Auto Sender

An automated tool for sending files and messages via WhatsApp Web.

## Features

- Automated file sending through WhatsApp Web
- GUI interface for monitoring and control
- Configurable folder monitoring
- Robust error handling and retry mechanisms
- Detailed logging with rotation
- Screenshot capture for debugging

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/whatsapp-auto-sender.git
cd whatsapp-auto-sender
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the application:
- Copy `config.yaml.example` to `config.yaml`
- Update the configuration values as needed

## Usage

1. Start the application:
```bash
python src/main.py
```

2. The GUI will appear with the following features:
- Monitor folder status
- Start/Stop monitoring
- Recent activity log
- Error notifications

3. Place files in the monitored folder to trigger automatic sending

## Configuration

Edit `resources/config.yaml` to configure:
- Monitored folder path
- Default message
- Retry settings
- Logging options
- Image paths for UI automation

## Project Structure

```
WhatsAppAutoSender/
├── src/
│   ├── core/           # Core functionality
│   ├── whatsapp/       # WhatsApp interaction
│   ├── gui/            # GUI components
│   └── main.py         # Entry point
├── resources/
│   ├── images/         # UI automation images
│   └── config.yaml     # Configuration
├── tests/              # Test files
├── logs/               # Application logs
├── error_screenshots/  # Error screenshots
├── requirements.txt    # Dependencies
└── README.md          # Documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Mohamed Ibrahim Moselhy - Senior RPA Developer 