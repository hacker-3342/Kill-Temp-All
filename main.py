import sys
import os
import json
import configparser
import threading
import shutil
import glob

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QToolBar, QComboBox, QCheckBox, QProgressBar, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt

class TempFileDeleter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Temp File Deleter")
        self.resize(700, 500)

        self.username = os.environ.get("USERNAME") or os.environ.get("USER")
        self.config = configparser.ConfigParser()
        self.config_file = os.path.join(os.path.dirname(__file__), 'settings.ini')
        self.load_language()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.create_toolbar()
        self.create_ui()

        self.files_deleted = 0
        self.folders_deleted = 0

    def load_language(self):
        self.config.read(self.config_file)
        language = self.config.get('Settings', 'language', fallback='english')
        language_file = os.path.join(os.path.dirname(__file__), 'Languages', f'{language}.json')
        with open(language_file, 'r') as f:
            self.lang = json.load(f)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Language dropdown
        self.language_combo = QComboBox()
        languages_dir = os.path.join(os.path.dirname(__file__), 'Languages')
        languages = [os.path.basename(f).split('.')[0] for f in glob.glob(os.path.join(languages_dir, '*.json'))]
        self.language_combo.addItems(languages)
        self.language_combo.setCurrentText(self.config.get('Settings', 'language', fallback='english'))
        self.language_combo.currentIndexChanged.connect(self.change_language)

        toolbar.addWidget(self.language_combo)

        # Save settings button
        save_button = QPushButton(self.lang["save_settings"])
        save_button.clicked.connect(self.save_settings)
        toolbar.addWidget(save_button)

    def create_ui(self):
        # Title
        title = QLabel(self.lang["title"])
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(title)

        # Description
        desc = QLabel(self.lang["description"])
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("font-size: 12px; color: gray;")
        self.layout.addWidget(desc)

        # Checkboxes
        self.checkboxes = {}
        for key in ["d_drive", "d_ame", "d_extensions", "c_drive", "c_ame", "c_extensions", "e_drive", "adobe_cache"]:
            cb = QCheckBox(self.lang.get(key, key))
            self.checkboxes[key] = cb
            self.layout.addWidget(cb)

        # Delete buttons
        btn_layout = QHBoxLayout()
        self.delete_btn = QPushButton(self.lang["delete_files"])
        self.delete_btn.clicked.connect(lambda: self.start_deletion(shutdown=False))
        btn_layout.addWidget(self.delete_btn)

        self.delete_shutdown_btn = QPushButton(self.lang["delete_files_shutdown"])
        self.delete_shutdown_btn.clicked.connect(lambda: self.start_deletion(shutdown=True))
        btn_layout.addWidget(self.delete_shutdown_btn)

        self.layout.addLayout(btn_layout)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(separator)

        # Progress bar and labels
        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

    def save_settings(self):
        self.config['Settings'] = {'language': self.language_combo.currentText()}
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile())
        QMessageBox.information(self, "Settings", "Settings saved!")

    def change_language(self):
        self.config['Settings'] = {'language': self.language_combo.currentText()}
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        QMessageBox.information(self, "Language", "Language changed! Please restart the app to apply.")

    def start_deletion(self, shutdown=False):
        self.progress_bar.setValue(0)
        threading.Thread(target=self.delete_files, args=(shutdown,), daemon=True).start()

        def delete_files(self, shutdown=False):
        # Simulate work (replace with your real deletion code later)
            import time
            for i in range(101):
                time.sleep(0.02)
                self.progress_bar.setValue(i)

            # When done:
            self.progress_bar.setValue(100)
            self.status_label.setText(self.lang.get("operation_completed", "Operation completed."))
        
            # Show success popup
            QMessageBox.information(self, "Done!", "Files deleted successfully!")

            if shutdown:
                # In Linux, shutdown via systemctl
                os.system("systemctl poweroff")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # DARK THEME 🌑
    dark_stylesheet = """
        QWidget {
            background-color: #121212;
            color: #e0e0e0;
        }
        QPushButton {
            background-color: #333333;
            color: #e0e0e0;
            border: 1px solid #555555;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #444444;
        }
        QProgressBar {
            border: 1px solid #555;
            border-radius: 5px;
            background-color: #333;
        }
        QProgressBar::chunk {
            background-color: #00bcd4;
            width: 10px;
        }
        QToolBar {
            background-color: #1f1f1f;
            spacing: 10px;
        }
        QComboBox {
            background-color: #333;
            color: #e0e0e0;
            padding: 3px;
        }
    """
    app.setStyleSheet(dark_stylesheet)

    window = TempFileDeleter()
    window.show()
    sys.exit(app.exec())

