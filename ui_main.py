from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QSpinBox, QTextEdit, QMessageBox, QProgressDialog, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QIcon, QColor, QFont
from account_manager import account_manager
from group_manager import group_manager
from config import config
import asyncio

class BatmanMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.new_event_loop()
        self.initUI()
        self.load_accounts_list()

    def initUI(self):
        self.setWindowTitle("Batman - Telegram Multi-Account Manager")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(self.get_main_stylesheet())

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(self.create_accounts_tab(), "Accounts")
        tabs.addTab(self.create_groups_tab(), "Groups")
        tabs.addTab(self.create_broadcast_tab(), "Broadcast")
        tabs.addTab(self.create_logs_tab(), "Logs")

        main_layout.addWidget(tabs)

        central_widget.setLayout(main_layout)

    def create_header(self):
        header = QWidget()
        layout = QHBoxLayout()

        title = QLabel("🦇 Batman - Telegram Bot Manager")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        layout.addStretch()

        status = QLabel("Status: Ready")
        status.setStyleSheet("color: #27ae60; font-weight: bold;")
        self.status_label = status
        layout.addWidget(status)

        header.setLayout(layout)
        header.setStyleSheet("background-color: #2c3e50; padding: 10px;")
        return header

    def create_accounts_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Add account section
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel("Phone Number:"))
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("+1234567890")
        add_layout.addWidget(self.phone_input)

        add_btn = QPushButton("Add Account")
        add_btn.clicked.connect(self.add_account)
        add_btn.setStyleSheet(self.get_button_stylesheet("#27ae60"))
        add_layout.addWidget(add_btn)

        layout.addLayout(add_layout)

        # Accounts list
        layout.addWidget(QLabel("Connected Accounts:"))
        self.accounts_list = QListWidget()
        self.accounts_list.itemClicked.connect(self.on_account_selected)
        layout.addWidget(self.accounts_list)

        # Account actions
        actions_layout = QHBoxLayout()

        verify_btn = QPushButton("Verify Code")
        verify_btn.clicked.connect(self.verify_account_code)
        verify_btn.setStyleSheet(self.get_button_stylesheet("#3498db"))
        actions_layout.addWidget(verify_btn)

        disconnect_btn = QPushButton("Disconnect")
        disconnect_btn.clicked.connect(self.disconnect_account)
        disconnect_btn.setStyleSheet(self.get_button_stylesheet("#e74c3c"))
        actions_layout.addWidget(disconnect_btn)

        remove_btn = QPushButton("Remove Account")
        remove_btn.clicked.connect(self.remove_account)
        remove_btn.setStyleSheet(self.get_button_stylesheet("#c0392b"))
        actions_layout.addWidget(remove_btn)

        layout.addLayout(actions_layout)

        widget.setLayout(layout)
        return widget

    def create_groups_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Load groups section
        load_layout = QHBoxLayout()
        load_layout.addWidget(QLabel("Select Account:"))

        self.account_combo = QLineEdit()
        self.account_combo.setReadOnly(True)
        load_layout.addWidget(self.account_combo)

        load_btn = QPushButton("Load Groups")
        load_btn.clicked.connect(self.load_groups)
        load_btn.setStyleSheet(self.get_button_stylesheet("#9b59b6"))
        load_layout.addWidget(load_btn)

        layout.addLayout(load_layout)

        # Groups list
        layout.addWidget(QLabel("Available Groups:"))
        self.groups_list = QListWidget()
        self.groups_list.setSelectionMode(self.groups_list.SelectionMode.MultiSelection)
        layout.addWidget(self.groups_list)

        # Save button
        save_btn = QPushButton("Save Selected Groups")
        save_btn.clicked.connect(self.save_selected_groups)
        save_btn.setStyleSheet(self.get_button_stylesheet("#27ae60"))
        layout.addWidget(save_btn)

        widget.setLayout(layout)
        return widget

    def create_broadcast_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Message section
        layout.addWidget(QLabel("Message:"))
        self.message_text = QTextEdit()
        self.message_text.setMinimumHeight(150)
        layout.addWidget(self.message_text)

        # Delay section
        delay_layout = QHBoxLayout()
        delay_layout.addWidget(QLabel("Delay between messages (seconds):"))
        
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setMinimum(1)
        self.delay_spinbox.setMaximum(3600)
        self.delay_spinbox.setValue(5)
        delay_layout.addWidget(self.delay_spinbox)
        delay_layout.addStretch()

        layout.addLayout(delay_layout)

        # Options
        self.markdown_checkbox = QCheckBox("Use Markdown formatting")
        self.markdown_checkbox.setChecked(True)
        layout.addWidget(self.markdown_checkbox)

        # Send buttons
        buttons_layout = QHBoxLayout()

        preview_btn = QPushButton("Preview")
        preview_btn.clicked.connect(self.preview_message)
        preview_btn.setStyleSheet(self.get_button_stylesheet("#3498db"))
        buttons_layout.addWidget(preview_btn)

        broadcast_btn = QPushButton("Send to All Groups")
        broadcast_btn.clicked.connect(self.broadcast_message)
        broadcast_btn.setStyleSheet(self.get_button_stylesheet("#e74c3c"))
        buttons_layout.addWidget(broadcast_btn)

        layout.addLayout(buttons_layout)
        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def create_logs_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Activity Logs:"))
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        layout.addWidget(self.logs_text)

        clear_btn = QPushButton("Clear Logs")
        clear_btn.clicked.connect(lambda: self.logs_text.clear())
        clear_btn.setStyleSheet(self.get_button_stylesheet("#95a5a6"))
        layout.addWidget(clear_btn)

        widget.setLayout(layout)
        return widget

    def add_account(self):
        phone = self.phone_input.text().strip()
        if not phone:
            QMessageBox.warning(self, "Error", "Please enter a phone number")
            return

        success, message = account_manager.add_account(phone)
        if success:
            self.phone_input.clear()
            self.load_accounts_list()
            self.log(f"Account added: {phone}")
            self.add_account_step2(phone)
        else:
            QMessageBox.warning(self, "Error", message)

    def add_account_step2(self, phone):
        """Start authentication process"""
        asyncio.run_coroutine_threadsafe(
            self._async_add_account(phone),
            self.loop
        )

    async def _async_add_account(self, phone):
        success, message = await account_manager.connect_account(phone)
        self.log(f"{phone}: {message}")
        if not success and "Code sent" in message:
            QMessageBox.information(self, "Verification", message)

    def verify_account_code(self):
        code, ok = self.get_input_dialog("Enter verification code:")
        if ok and code:
            selected = self.accounts_list.currentItem()
            if selected:
                phone = selected.text().split(" - ")[0]
                asyncio.run_coroutine_threadsafe(
                    self._async_verify_code(phone, code),
                    self.loop
                )

    async def _async_verify_code(self, phone, code):
        success, message = await account_manager.verify_code(phone, code)
        self.log(f"{phone}: {message}")
        if success:
            QMessageBox.information(self, "Success", message)
            self.load_accounts_list()
        else:
            QMessageBox.warning(self, "Error", message)

    def disconnect_account(self):
        selected = self.accounts_list.currentItem()
        if selected:
            phone = selected.text().split(" - ")[0]
            asyncio.run_coroutine_threadsafe(
                account_manager.disconnect_account(phone),
                self.loop
            )
            self.log(f"Disconnected: {phone}")

    def remove_account(self):
        selected = self.accounts_list.currentItem()
        if selected:
            phone = selected.text().split(" - ")[0]
            reply = QMessageBox.question(self, "Confirm", f"Remove {phone}?")
            if reply == QMessageBox.StandardButton.Yes:
                account_manager.remove_account(phone)
                self.load_accounts_list()
                self.log(f"Account removed: {phone}")

    def load_accounts_list(self):
        self.accounts_list.clear()
        accounts = account_manager.get_accounts()
        for acc in accounts:
            item = QListWidgetItem(f"{acc['phone']} - {acc['status']}")
            self.accounts_list.addItem(item)

    def on_account_selected(self, item):
        phone = item.text().split(" - ")[0]
        self.account_combo.setText(phone)

    def load_groups(self):
        phone = self.account_combo.text().strip()
        if not phone:
            QMessageBox.warning(self, "Error", "Please select an account")
            return

        asyncio.run_coroutine_threadsafe(
            self._async_load_groups(phone),
            self.loop
        )

    async def _async_load_groups(self, phone):
        client = await account_manager.get_client(phone)
        if not client:
            self.log(f"Error: Cannot connect to {phone}")
            return

        groups = await group_manager.load_groups(client)
        self.groups_list.clear()

        for group in groups:
            item = QListWidgetItem(group['title'])
            item.setData(Qt.ItemDataRole.UserRole, group)
            self.groups_list.addItem(item)

        self.log(f"Loaded {len(groups)} groups from {phone}")

    def save_selected_groups(self):
        phone = self.account_combo.text().strip()
        if not phone:
            QMessageBox.warning(self, "Error", "Please select an account")
            return

        selected_items = self.groups_list.selectedItems()
        groups = [item.data(Qt.ItemDataRole.UserRole) for item in selected_items]

        account_manager.update_groups(phone, groups)
        self.log(f"Saved {len(groups)} groups for {phone}")
        QMessageBox.information(self, "Success", f"Saved {len(groups)} groups")

    def preview_message(self):
        message = self.message_text.toPlainText()
        if not message:
            QMessageBox.warning(self, "Error", "Message is empty")
            return

        QMessageBox.information(self, "Message Preview", message)

    def broadcast_message(self):
        message = self.message_text.toPlainText()
        if not message:
            QMessageBox.warning(self, "Error", "Message is empty")
            return

        delay = self.delay_spinbox.value()
        asyncio.run_coroutine_threadsafe(
            self._async_broadcast(message, delay),
            self.loop
        )

    async def _async_broadcast(self, message, delay):
        accounts = account_manager.get_accounts()
        total_sent = 0

        for account in accounts:
            phone = account['phone']
            client = await account_manager.get_client(phone)

            if not client:
                self.log(f"Skipping {phone}: Not connected")
                continue

            for group in account['groups']:
                try:
                    await group_manager.send_message(client, group['entity'], message)
                    total_sent += 1
                    self.log(f"Message sent to {group['title']} from {phone}")

                    # Wait before next message
                    import time
                    time.sleep(delay)

                except Exception as e:
                    self.log(f"Error sending to {group['title']}: {str(e)}")

        self.log(f"\nBroadcast complete! Total messages sent: {total_sent}")
        QMessageBox.information(self, "Complete", f"Broadcast complete! {total_sent} messages sent")

    def log(self, message):
        self.logs_text.append(message)

    def get_input_dialog(self, prompt):
        from PyQt6.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(self, "Input", prompt)
        return text, ok

    @staticmethod
    def get_main_stylesheet():
        return """
        QMainWindow {
            background-color: #ecf0f1;
        }
        QLabel {
            color: #2c3e50;
            font-size: 12px;
        }
        QLineEdit, QTextEdit, QSpinBox {
            padding: 6px;
            border: 1px solid #bdc3c7;
            border-radius: 3px;
            background-color: white;
            color: #2c3e50;
        }
        QLineEdit:focus, QTextEdit:focus {
            border: 2px solid #3498db;
        }
        QListWidget {
            border: 1px solid #bdc3c7;
            border-radius: 3px;
            background-color: white;
        }
        QListWidget::item:selected {
            background-color: #3498db;
            color: white;
        }
        QTabWidget::pane {
            border: 1px solid #bdc3c7;
        }
        QTabBar::tab {
            background-color: #95a5a6;
            color: white;
            padding: 6px 20px;
        }
        QTabBar::tab:selected {
            background-color: #3498db;
        }
        QCheckBox {
            color: #2c3e50;
            spacing: 5px;
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
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: {color}dd;
        }}
        QPushButton:pressed {{
            background-color: {color}99;
        }}
        """
