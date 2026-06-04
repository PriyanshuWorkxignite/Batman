#!/usr/bin/env python3
import sys
import asyncio
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from config import config
from ui_setup import SetupDialog
from ui_main import BatmanMainWindow

def start_event_loop():
    """Start asyncio event loop in a separate thread"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    def run_loop():
        loop.run_forever()
    
    import threading
    thread = threading.Thread(target=run_loop, daemon=True)
    thread.start()
    return loop

def main():
    # Create QApplication with optimized settings
    app = QApplication(sys.argv)
    
    # Performance optimizations for localhost
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseStyleSheetPropagationInWidgetStyles, True)

    # Start event loop for async operations
    loop = start_event_loop()

    # Show setup dialog if not configured
    if not config.is_configured():
        setup_dialog = SetupDialog()
        if setup_dialog.exec() != SetupDialog.DialogCode.Accepted:
            sys.exit(0)

    # Show main window
    main_window = BatmanMainWindow()
    main_window.loop = loop
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
