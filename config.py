import os
import json
from pathlib import Path

# Configuration file paths
CONFIG_DIR = Path.home() / ".batman"
CONFIG_FILE = CONFIG_DIR / "config.json"
SESSIONS_DIR = CONFIG_DIR / "sessions"

# Create necessary directories
CONFIG_DIR.mkdir(exist_ok=True)
SESSIONS_DIR.mkdir(exist_ok=True)

class Config:
    def __init__(self):
        self.api_id = None
        self.api_hash = None
        self.load_config()

    def load_config(self):
        """Load configuration from file"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                self.api_id = config.get('api_id')
                self.api_hash = config.get('api_hash')

    def save_config(self, api_id, api_hash):
        """Save configuration to file"""
        config = {
            'api_id': api_id,
            'api_hash': api_hash
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        self.api_id = api_id
        self.api_hash = api_hash

    def is_configured(self):
        """Check if API credentials are configured"""
        return self.api_id is not None and self.api_hash is not None

    @staticmethod
    def get_session_path(phone_number):
        """Get session file path for a phone number"""
        return SESSIONS_DIR / f"{phone_number}.session"

# Global config instance
config = Config()
