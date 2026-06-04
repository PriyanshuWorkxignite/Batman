from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from config import config

class SetupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Batman - Initial Setup")
        self.setGeometry(100, 100, 500, 250)
        self.setStyleSheet(self.get_stylesheet())

        layout = QVBoxLayout()

        # Title
        title = QLabel("Telegram API Configuration")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        # API ID
        api_id_label = QLabel("API ID:")
        self.api_id_input = QLineEdit()
        self.api_id_input.setPlaceholderText("Enter your API ID from my.telegram.org")
        layout.addWidget(api_id_label)
        layout.addWidget(self.api_id_input)

        # API Hash
        api_hash_label = QLabel("API Hash:")
        self.api_hash_input = QLineEdit()
        self.api_hash_input.setPlaceholderText("Enter your API Hash from my.telegram.org")
        layout.addWidget(api_hash_label)
        layout.addWidget(self.api_hash_input)

        # Info
        info = QLabel(
            "Get your API credentials from https://my.telegram.org\n"
            "1. Go to the website and login with your Telegram account\n"
            "2. Go to 'API development tools'\n"
            "3. Create a new application\n"
            "4. Copy API ID and API Hash here"
        )
        info.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        layout.addWidget(info)

        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save & Continue")
        save_btn.clicked.connect(self.save_credentials)
        save_btn.setStyleSheet(self.get_button_stylesheet("#3498db"))
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_credentials(self):
        api_id = self.api_id_input.text().strip()
        api_hash = self.api_hash_input.text().strip()

        if not api_id or not api_hash:
            QMessageBox.warning(self, "Validation Error", "Please enter both API ID and API Hash")
            return

        try:
            api_id = int(api_id)
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "API ID must be a number")
            return

        config.save_config(api_id, api_hash)
        QMessageBox.information(self, "Success", "Configuration saved successfully!")
        self.accept()

    @staticmethod
    def get_stylesheet():
        return """
        QDialog {
            background-color: #ecf0f1;
        }
        QLabel {
            color: #2c3e50;
            font-size: 12px;
        }
        QLineEdit {
            padding: 8px;
            border: 2px solid #3498db;
            border-radius: 4px;
            background-color: white;
            color: #2c3e50;
            font-size: 12px;
        }
        QLineEdit:focus {
            border: 2px solid #2980b9;
        }
        """

    @staticmethod
    def get_button_stylesheet(color):
        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {color}dd;
        }}
        QPushButton:pressed {{
            background-color: {color}99;
        }}
        """
