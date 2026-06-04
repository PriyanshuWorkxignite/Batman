```markdown
# 🦇 Batman - Telegram Multi-Account Manager

A powerful Python application for managing multiple Telegram accounts simultaneously, with features for batch messaging, session management, and group management.

## Features

✨ **Multi-Account Management**
- Add and manage multiple Telegram accounts
- Persistent session storage
- Automatic authentication handling
- 2FA support

📱 **Group Management**
- Load all groups from any account
- Select multiple groups for broadcasting
- Easy group filtering and selection
- Real-time group synchronization

📢 **Batch Messaging**
- Send messages to multiple groups simultaneously
- Configurable delays between messages to avoid Telegram restrictions
- Message preview functionality
- Markdown formatting support
- Broadcast history and logging

🎨 **Modern UI**
- Clean, intuitive PyQt6 interface
- Dark theme with color-coded elements
- Real-time activity logs
- Responsive design

🔐 **Security**
- Sessions stored locally
- No credentials stored in plain text
- API credentials configured on first run
- Secure authentication flow

## Requirements

- Python 3.8+
- Telegram account
- API credentials from https://my.telegram.org

## Installation

1. Clone the repository:
```bash
git clone https://github.com/PriyanshuWorkxignite/Batman.git
cd Batman
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup

### Getting Telegram API Credentials

1. Go to https://my.telegram.org
2. Log in with your Telegram account
3. Click on "API development tools"
4. Create a new application if you don't have one
5. Copy your **API ID** and **API Hash**

### First Run

When you run the application for the first time, it will ask for your API credentials:

```bash
python main.py
```

A setup dialog will appear. Enter your API ID and API Hash, then click "Save & Continue".

## Usage

### Adding an Account

1. Go to the **Accounts** tab
2. Enter the phone number (with country code, e.g., +1234567890)
3. Click "Add Account"
4. Telegram will send a verification code to your phone
5. In the application, click "Verify Code" and enter the code
6. If 2FA is enabled, follow the additional authentication steps

### Loading Groups

1. Go to the **Groups** tab
2. Select an account from the dropdown
3. Click "Load Groups"
4. Wait for the groups to load (this may take a few seconds)
5. Select the groups you want to send messages to
6. Click "Save Selected Groups"

### Broadcasting Messages

1. Go to the **Broadcast** tab
2. Enter your message in the text area
3. Set the delay between messages (in seconds)
4. Enable/disable Markdown formatting as needed
5. Click "Preview" to see how the message will look
6. Click "Send to All Groups" to broadcast

**Note:** Use at least 2-3 seconds delay to avoid hitting Telegram rate limits.

### Checking Logs

1. Go to the **Logs** tab
2. View all activity from the application
3. Click "Clear Logs" to clear the log history

## Message Formatting

The application supports Markdown formatting:

```
**bold**
*italic*
__underline__
~~strikethrough~~
`inline code`
```​`
code block
`​``

[Link](https://example.com)
```

## Safety Tips

⚠️ **Important:**
- Do NOT use extremely short delays (less than 2 seconds)
- Space out messages to different groups
- Avoid broadcasting identical messages repeatedly
- Use realistic delays (3-10 seconds recommended)
- Telegram may temporarily limit accounts if rate limits are exceeded

## File Structure

```
Batman/
├── main.py                 # Application entry point
├── config.py              # Configuration management
├── account_manager.py     # Account and session handling
├── group_manager.py       # Group loading and messaging
├── ui_setup.py           # Initial setup dialog
├── ui_main.py            # Main application UI
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Configuration

Configuration files are stored in your home directory:
- `~/.batman/config.json` - API credentials
- `~/.batman/accounts.json` - Account information
- `~/.batman/sessions/` - Telegram session files

## Troubleshooting

### "Code sent to Telegram app" but no code appears
- Check your Telegram app for incoming messages
- Make sure you're using the correct phone number
- Try logging out and back into Telegram

### "Connection error" when adding account
- Verify your API credentials are correct
- Check your internet connection
- Make sure Telegram is not blocking your connection

### Groups not loading
- Ensure the account is fully authenticated
- Try disconnecting and reconnecting the account
- Check that you have permission to access the groups

### Messages not being sent
- Verify the selected groups are correct
- Check that the account has permission to send messages
- Review the logs for specific error messages
- Increase the delay between messages

## Performance

- Loading 200+ groups may take 30-60 seconds
- Message sending speed depends on your internet connection
- Delays are enforced to prevent rate limiting

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is provided as-is for educational and personal use.

## Disclaimer

This tool is for legitimate purposes only. Users are responsible for complying with Telegram's terms of service and local laws. The authors are not responsible for any misuse of this tool.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the logs for detailed error messages
3. Open an issue on GitHub

---

**Made with ❤️ for Telegram automation**
```
