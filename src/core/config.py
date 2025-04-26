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
            'TempMessageForGroupPath',
            'retry_attempts',
            'retry_delay',
            'timeout',
            'wait_time'
        ]
        
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"Missing required configuration field: {field}")
        
    def create_default_config(self) -> None:
        """Create default configuration file"""
        default_config = {
            'folder_to_watch': 'C:\\Users\\Lenovo\\OneDrive - Giza Systems\\قضايا التحكيم\\منظورة تجربة',
            'root_path': "https://gizasystems-my.sharepoint.com/personal/mohamed_moselhy_gizasystems_com/Documents/%D9%82%D8%B6%D9%8A%D8%A7%D9%8A%D8%A7%20%D8%A7%D9%84%D8%AA%D8%AD%D9%83%D9%8A%D9%85/%D9%85%D9%86%D9%8F%D8%B8%D9%88%D8%B1%D9%8E%D8%A9%20%D8%AA%D8%AC%D8%B1%D8%A8%D8%A9",
            'retry_attempts': 3,
            'retry_delay': 5,
            'timeout': 30,
            'wait_time': 2,
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(levelname)s - %(message)s',
                'max_size': 10485760,  # 10MB
                'backup_count': 5
            },
            'TempMessageForGroupPath': r'src\MessageTemplates\NotificationToGroup.txt'
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

    def read_value(self, key: str, default: Any = None) -> Any:
        """Method to directly read a config value"""
        return self.config.get(key, default)

    def set_value(self, key: str, value: Any) -> None:
        """Method to set a new value in the config"""
        self.config[key] = value
        self.save_config()

    def save_config(self) -> None:
        """Save the updated configuration to the YAML file"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False)

# Create global config instance
config = Config()
