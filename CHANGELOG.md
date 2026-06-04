# Changelog

All notable changes to the Batman project will be documented in this file.

## [1.0.0] - 2024-06-04

### Added

#### Core Features
- Multi-account Telegram management
- Persistent session storage with local encryption
- Real-time account connection management
- Support for 2FA-enabled accounts

#### Account Management
- Add multiple Telegram accounts
- Remove and disconnect accounts
- Account status tracking
- Session persistence across application restarts
- Automatic reconnection on startup

#### Group Management
- Load all groups and channels from selected accounts
- Multi-group selection for batch operations
- Group filtering and search
- Save selected groups per account
- Support for both channels and regular groups

#### Batch Messaging (Broadcasting)
- Send messages to multiple groups simultaneously
- Configurable delay between messages (1-3600 seconds)
- Markdown formatting support
- Message preview functionality
- Safety delays to prevent Telegram rate limiting
- Detailed broadcast statistics

#### Security Features
- API credentials configuration on first run
- Local session storage
- No plain-text credential storage
- Secure authentication flow
- 2FA password handling

#### User Interface
- Modern PyQt6-based GUI
- Clean, intuitive design
- Dark color scheme with good contrast
- Real-time activity logging
- Responsive tab-based layout
- Input validation
- Progress and status indicators

#### Logging & Monitoring
- Real-time activity logs
- Message sending history
- Error reporting
- Account connection status
- Broadcast statistics

### Features Details

**Accounts Tab:**
- Add account with phone number
- Verify authentication code
- Verify 2FA password
- Disconnect account
- Remove account with session cleanup
- Account list with status

**Groups Tab:**
- Select account from list
- Load groups from account
- Multi-select groups
- Save group selection
- Group title and type display

**Broadcast Tab:**
- Rich text editor for messages
- Markdown formatting preview
- Delay configuration
- Format support toggle
- Send to all groups
- Message preview

**Logs Tab:**
- Real-time activity feed
- Clear logs functionality
- Timestamped entries
- Error and success messages

### Configuration
- API ID and Hash setup on first run
- Configuration saved in ~/.batman/config.json
- Accounts saved in ~/.batman/accounts.json
- Sessions stored in ~/.batman/sessions/

### Technical Details
- Built with Python 3.8+
- Uses Telethon for Telegram client library
- PyQt6 for modern GUI
- Asyncio for async operations
- Session management with TelegramClient

## Future Roadmap

### v1.1.0 (Planned)
- [ ] Scheduled message sending
- [ ] Message templates
- [ ] Advanced group filtering
- [ ] Broadcast statistics dashboard
- [ ] Export logs to file
- [ ] Import/export group lists

### v1.2.0 (Planned)
- [ ] Direct message support
- [ ] Media attachment support
- [ ] Bulk group operations
- [ ] Account duplication
- [ ] Advanced error recovery

### v2.0.0 (Planned)
- [ ] Web-based UI alternative
- [ ] REST API for automation
- [ ] Database backend for analytics
- [ ] Docker containerization
- [ ] Multi-language support

## Known Limitations

1. **Telegram Rate Limits:** 
   - Minimum 2-second delay recommended between messages
   - Account-level rate limiting may apply

2. **Session Management:**
   - Sessions stored locally, not synced across devices
   - First login requires authentication code

3. **Group Loading:**
   - Large accounts (500+ groups) may take time to load
   - Channel-only accounts may have limited loading speed

## Migration from v0.x

N/A - Initial release as v1.0.0

## Contributors

- Priyanshu (Initial development)

## License

This project is provided as-is for educational and personal use.

---

**For bug reports and feature requests, please open an issue on GitHub.**
