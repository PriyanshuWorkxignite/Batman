import json
from pathlib import Path
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from config import config, CONFIG_DIR

ACCOUNTS_FILE = CONFIG_DIR / "accounts.json"

class AccountManager:
    def __init__(self):
        self.accounts = self.load_accounts()
        self.clients = {}

    def load_accounts(self):
        """Load saved accounts from file"""
        if ACCOUNTS_FILE.exists():
            with open(ACCOUNTS_FILE, 'r') as f:
                return json.load(f)
        return []

    def save_accounts(self):
        """Save accounts to file"""
        with open(ACCOUNTS_FILE, 'w') as f:
            json.dump(self.accounts, f, indent=4)

    def add_account(self, phone_number):
        """Add a new account"""
        if self._account_exists(phone_number):
            return False, "Account already exists"

        self.accounts.append({
            'phone': phone_number,
            'status': 'connected',
            'groups': []
        })
        self.save_accounts()
        return True, f"Account {phone_number} added successfully"

    def _account_exists(self, phone_number):
        """Check if account already exists"""
        return any(acc['phone'] == phone_number for acc in self.accounts)

    def remove_account(self, phone_number):
        """Remove an account"""
        self.accounts = [acc for acc in self.accounts if acc['phone'] != phone_number]
        self.save_accounts()

        # Remove session file
        session_path = config.get_session_path(phone_number)
        if session_path.exists():
            session_path.unlink()

    def get_accounts(self):
        """Get all accounts"""
        return self.accounts

    async def connect_account(self, phone_number):
        """Connect to Telegram account"""
        if not config.is_configured():
            return False, "API credentials not configured"

        try:
            session_path = str(config.get_session_path(phone_number))
            
            client = TelegramClient(session_path, config.api_id, config.api_hash)
            await client.connect()

            if not await client.is_user_authorized():
                # Start authentication
                await client.send_code_request(phone_number)
                return False, "Code sent to Telegram app"

            self.clients[phone_number] = client
            return True, "Connected successfully"

        except Exception as e:
            return False, f"Connection error: {str(e)}"

    async def verify_code(self, phone_number, code):
        """Verify authentication code"""
        try:
            session_path = str(config.get_session_path(phone_number))
            client = TelegramClient(session_path, config.api_id, config.api_hash)
            await client.connect()

            try:
                await client.sign_in(phone_number, code)
            except SessionPasswordNeededError:
                return False, "2FA enabled. Password required"

            self.clients[phone_number] = client
            return True, "Verified successfully"

        except Exception as e:
            return False, f"Verification error: {str(e)}"

    async def verify_password(self, phone_number, password):
        """Verify 2FA password"""
        try:
            session_path = str(config.get_session_path(phone_number))
            client = TelegramClient(session_path, config.api_id, config.api_hash)
            await client.connect()

            await client.sign_in(password=password)
            self.clients[phone_number] = client
            return True, "2FA verified successfully"

        except Exception as e:
            return False, f"2FA verification error: {str(e)}"

    async def get_client(self, phone_number):
        """Get or create client for account"""
        if phone_number in self.clients:
            return self.clients[phone_number]

        session_path = str(config.get_session_path(phone_number))
        client = TelegramClient(session_path, config.api_id, config.api_hash)
        await client.connect()

        if await client.is_user_authorized():
            self.clients[phone_number] = client
            return client
        return None

    async def disconnect_account(self, phone_number):
        """Disconnect account"""
        if phone_number in self.clients:
            await self.clients[phone_number].disconnect()
            del self.clients[phone_number]

    def update_groups(self, phone_number, groups):
        """Update groups for an account"""
        for acc in self.accounts:
            if acc['phone'] == phone_number:
                acc['groups'] = groups
                break
        self.save_accounts()

# Global account manager
account_manager = AccountManager()
