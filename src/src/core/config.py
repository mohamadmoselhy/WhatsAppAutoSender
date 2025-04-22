"""
Configuration management for WhatsApp Auto Sender
"""

import os
import yaml
from typing import Dict, Any
from pathlib import Path

class Config:
    def __init__(self, config_path: str = "resources/config.yaml"):
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            self.validate_config()
        except FileNotFoundError:
            self.create_default_config()
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration: {e}")

    def validate_config(self) -> None:
        """Validate the configuration"""
        required_fields = [
            'folder_to_watch',
            'default_contact',
            'message',
            'images',
            'retry_attempts',
            'retry_delay',
            'timeout',
            'wait_time'
        ]
        
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"Missing required configuration field: {field}")

        # Validate images configuration
        required_images = [
            'search_field_image',
            'search_input',
            'attachment',
            'document',
            'whatsapp_images',
            'message_box'
        ]
        
        if 'images' not in self.config:
            raise ValueError("Missing 'images' configuration section")
            
        for image in required_images:
            if image not in self.config['images']:
                raise ValueError(f"Missing required image configuration: {image}")

    def create_default_config(self) -> None:
        """Create default configuration file"""
        default_config = {
            'folder_to_watch': 'C:\\Users\\Lenovo\\OneDrive - Giza Systems\\قضايا التحكيم\\منظورة تجربة',
            'default_contact': 'Default Contact',
            'message': 'Please find the attached file',
            'images': {
                'search_field_image': 'resources/images/search_field.png',
                'search_input': 'resources/images/search_input.png',
                'search_input2': 'resources/images/search_input2.png',
                'attachment': 'resources/images/attachment.png',
                'document': 'resources/images/document.png',
                'whatsapp_images': 'resources/images/whatsapp_images.png',
                'message_box': 'resources/images/message_box.png'
            },
            'retry_attempts': 3,
            'retry_delay': 5,
            'timeout': 30,
            'wait_time': 2,
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(levelname)s - %(message)s',
                'max_size': 10485760,  # 10MB
                'backup_count': 5
            }
        }
        
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        self.config = default_config

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with optional default"""
        return self.config.get(key, default)

    def __getattr__(self, name: str) -> Any:
        """Allow direct access to config values as attributes"""
        if name in self.config:
            return self.config[name]
        raise AttributeError(f"Configuration has no attribute '{name}'")

# Create global config instance
config = Config() 