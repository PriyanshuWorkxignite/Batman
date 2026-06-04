# Installation Guide for Batman

## System Requirements

- **Python Version:** 3.8 or higher
- **Operating System:** Windows, macOS, or Linux
- **RAM:** 512 MB minimum
- **Disk Space:** 100 MB minimum
- **Internet:** Stable connection required

## Step-by-Step Installation

### 1. Install Python

#### Windows
- Download Python from https://www.python.org/downloads/
- Run the installer
- **Important:** Check "Add Python to PATH"
- Click "Install Now"

#### macOS
- Install using Homebrew:
  ```bash
  brew install python3
  ```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### 2. Clone the Repository

```bash
git clone https://github.com/PriyanshuWorkxignite/Batman.git
cd Batman
```

### 3. Create Virtual Environment (Recommended)

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Get Telegram API Credentials

1. Go to https://my.telegram.org in your browser
2. Log in with your Telegram account
3. Navigate to "API development tools"
4. Create a new application:
   - App title: "Batman Telegram Manager" (or any name)
   - Short name: "batman_manager"
   - URL: Leave blank (unless you need one)
5. Copy the **API ID** and **API Hash**
6. Keep these safe - you'll need them when running the application

### 6. Run the Application

```bash
python main.py
```

On the first run, you'll see a setup dialog:
1. Enter your API ID
2. Enter your API Hash
3. Click "Save & Continue"

### 7. Add Your First Account

1. Go to the "Accounts" tab
2. Enter your phone number (with country code, e.g., +1234567890)
3. Click "Add Account"
4. Telegram will send a verification code
5. Click "Verify Code" and enter the code from your Telegram app
6. If you have 2FA enabled, enter your password when prompted

## Troubleshooting Installation

### Python not found
- **Windows:** Make sure you checked "Add Python to PATH" during installation
- **macOS/Linux:** Use `python3` instead of `python`

### pip command not found
```bash
python -m pip install --upgrade pip
```

### SSL/Certificate error on macOS
```bash
/Applications/Python\ 3.x/Install\ Certificates.command
```

### Permission denied on Linux
```bash
sudo pip3 install -r requirements.txt
```

### Virtual environment not activating
Try creating a new one:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

### ModuleNotFoundError when running
Make sure:
1. Virtual environment is activated (if using one)
2. All dependencies are installed: `pip install -r requirements.txt`
3. You're in the correct directory: `cd Batman`

## Verifying Installation

To verify everything is working:

```bash
# Check Python version
python --version

# Check pip is working
pip --version

# Test imports
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6: OK')"
python -c "import telethon; print('Telethon: OK')"
```

## Running Without Virtual Environment

If you prefer not to use a virtual environment, simply install globally:

```bash
pip install -r requirements.txt
python main.py
```

**Note:** Virtual environments are recommended for cleaner project isolation.

## Updating Dependencies

To update all dependencies to their latest versions:

```bash
pip install --upgrade -r requirements.txt
```

## Uninstallation

To completely remove Batman and its dependencies:

```bash
# If using virtual environment
deactivate
rm -rf venv

# Remove the repository
rm -rf Batman

# Remove configuration
rm -rf ~/.batman
```

## Need Help?

1. Check the main README.md
2. Review the logs in the application
3. Verify your Telegram API credentials
4. Ensure you have a stable internet connection

---

**Ready to use Batman!** 🦇
