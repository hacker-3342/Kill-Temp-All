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
from PyQt6.QtCore import Qt, QMetaObject, Q_ARG, pyqtSlot

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
        theme = self.config.get('Settings', 'theme', fallback='dark')
        self.theme = theme
        language_file = os.path.join(os.path.dirname(__file__), 'Languages', f'{language}.json')
        with open(language_file, 'r', encoding='utf-8') as f:
            self.lang = json.load(f)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        self.language_combo = QComboBox()
        languages_dir = os.path.join(os.path.dirname(__file__), 'Languages')
        languages = [os.path.basename(f).split('.')[0] for f in glob.glob(os.path.join(languages_dir, '*.json'))]
        self.language_combo.addItems(languages)
        self.language_combo.setCurrentText(self.config.get('Settings', 'language', fallback='english'))
        self.language_combo.currentIndexChanged.connect(self.change_language)
        toolbar.addWidget(self.language_combo)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        self.theme_combo.setCurrentText(self.theme)
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        toolbar.addWidget(self.theme_combo)

        save_button = QPushButton(self.lang["save_settings"])
        save_button.clicked.connect(self.save_settings)
        toolbar.addWidget(save_button)

    def create_ui(self):
        title = QLabel(self.lang["title"])
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px;")
        self.layout.addWidget(title)

        desc = QLabel(self.lang["description"])
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("font-size: 12px; color: gray;")
        self.layout.addWidget(desc)

        self.checkboxes = {}
        drive_sections = {
            "d_drive": ["d_ame", "d_extensions"],
            "c_drive": ["c_ame", "c_extensions"]
        }

        for drive, children in drive_sections.items():
            section_label = QLabel(self.lang.get(drive, drive))
            section_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
            self.layout.addWidget(section_label)

            for key in children:
                label = self.lang.get(key, key).replace("{username}", self.username)
                cb = QCheckBox(label)
                self.checkboxes[key] = cb
                self.layout.addWidget(cb)

        # Adobe cache as a special item
        label = self.lang.get("adobe_cache", "Adobe Cache").replace("{username}", self.username)
        cb = QCheckBox(label)
        self.checkboxes["adobe_cache"] = cb
        self.layout.addWidget(cb)

        btn_layout = QHBoxLayout()
        self.delete_btn = QPushButton(self.lang["delete_files"])
        self.delete_btn.clicked.connect(lambda: self.start_deletion(shutdown=False))
        btn_layout.addWidget(self.delete_btn)

        self.delete_shutdown_btn = QPushButton(self.lang["delete_files_shutdown"])
        self.delete_shutdown_btn.clicked.connect(lambda: self.start_deletion(shutdown=True))
        btn_layout.addWidget(self.delete_shutdown_btn)
        self.layout.addLayout(btn_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(separator)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

    def change_language(self):
        self.config['Settings'] = {'language': self.language_combo.currentText()}
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        QMessageBox.information(self, "Language", "Language changed! Please restart the app to apply.")

    def change_theme(self):
        self.theme = self.theme_combo.currentText()
        self.apply_theme()

    def apply_theme(self):
        theme_file = os.path.join(os.path.dirname(__file__), "styles", f"{self.theme}_theme.qss")
        with open(theme_file, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def save_settings(self):
        self.config['Settings'] = {
            'language': self.language_combo.currentText(),
            'theme': self.theme_combo.currentText()
        }
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        QMessageBox.information(self, "Settings", "Settings saved!")

    def start_deletion(self, shutdown=False):
        self.progress_bar.setValue(0)
        threading.Thread(target=self.delete_files, args=(shutdown,), daemon=True).start()

    def delete_files(self, shutdown=False):
        selected_tasks = [key for key, checkbox in self.checkboxes.items() if checkbox.isChecked()]

        if not selected_tasks:
            QMetaObject.invokeMethod(self, "show_no_tasks_popup", Qt.ConnectionType.QueuedConnection)
            return

        progress_increment = 100 // len(selected_tasks)
        current_progress = 0

        for task in selected_tasks:
            self.simulate_task(task)
            current_progress += progress_increment
            QMetaObject.invokeMethod(self.progress_bar, "setValue", Qt.ConnectionType.QueuedConnection, Q_ARG(int, current_progress))

        QMetaObject.invokeMethod(self.progress_bar, "setValue", Qt.ConnectionType.QueuedConnection, Q_ARG(int, 100))
        QMetaObject.invokeMethod(self.status_label, "setText", Qt.ConnectionType.QueuedConnection, Q_ARG(str, self.lang.get("operation_completed", "Operation completed.")))
        QMetaObject.invokeMethod(self, "show_popup", Qt.ConnectionType.QueuedConnection)

        if shutdown:
            os.system("shutdown /s /t 0")

    def simulate_task(self, task):
        paths = {
            "d_ame": ("D:/", "_AME"),
            "d_extensions": ("D:/", [".mpgindex", ".ims", ".cfa", ".pek"]),
            "c_ame": ("C:/", "_AME"),
            "c_extensions": ("C:/", [".mpgindex", ".ims", ".cfa", ".pek"]),
            "adobe_cache": (f"C:/Users/{self.username}/AppData/Roaming/Adobe/common/Media Cache Files", None),
        }

        if task not in paths:
            return

        path, condition = paths[task]
        if not os.path.exists(path):
            return

        for root, subdirs, files in os.walk(path, topdown=False):
            if condition is None:
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                        self.files_deleted += 1
                    except PermissionError:
                        pass
                for name in subdirs:
                    try:
                        shutil.rmtree(os.path.join(root, name))
                        self.folders_deleted += 1
                    except PermissionError:
                        pass
            elif isinstance(condition, str):
                for name in subdirs:
                    if name.endswith(condition):
                        try:
                            shutil.rmtree(os.path.join(root, name))
                            self.folders_deleted += 1
                        except PermissionError:
                            pass
            elif isinstance(condition, list):
                for name in files:
                    if any(name.endswith(ext) for ext in condition):
                        try:
                            os.remove(os.path.join(root, name))
                            self.files_deleted += 1
                        except PermissionError:
                            pass

    @pyqtSlot()
    def show_no_tasks_popup(self):
        QMessageBox.warning(self, self.lang.get("advisory", "Warning"), self.lang.get("no_tasks_selected", "No tasks were selected. Please select at least one task to proceed."))

    @pyqtSlot()
    def show_popup(self):
        QMessageBox.information(self, self.lang.get("operation_completed", "Operation completed"), self.lang.get("files_deleted_success", "Files deleted successfully!"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TempFileDeleter()
    window.apply_theme()
    window.show()
    sys.exit(app.exec())

