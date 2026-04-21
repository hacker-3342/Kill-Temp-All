import sys
import os
import json
import configparser
import threading 
import shutil
import glob
import math
import psutil  # Add this import at the top

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QToolBar,
    QComboBox,
    QCheckBox,
    QProgressBar,
    QFrame,
    QMessageBox,
    QTabWidget
)
from PyQt6.QtCore import Qt, QMetaObject, Q_ARG, pyqtSlot
from PyQt6.QtGui import QIcon

class TempFileDeleter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Temp File Deleter")
        self.resize(700, 350)

        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), "logo.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.username = os.environ.get("USERNAME") or os.environ.get("USER")
        self.config = configparser.ConfigParser()
        self.config_file = os.path.join(os.path.dirname(__file__), "settings.ini")
        self.load_language()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.create_toolbar()
        self.create_ui()

        self.files_deleted = 0
        self.folders_deleted = 0
        self.space_cleared = 0  # Track total bytes cleared

    def load_language(self):
        self.config.read(self.config_file)
        language = self.config.get("Settings", "language", fallback="english")
        theme = self.config.get("Settings", "theme", fallback="dark")
        self.theme = theme
        language_file = os.path.join(
            os.path.dirname(__file__), "Languages", f"{language}.json"
        )
        with open(language_file, "r", encoding="utf-8") as f:
            self.lang = json.load(f)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        self.language_combo = QComboBox()
        languages_dir = os.path.join(os.path.dirname(__file__), "Languages")
        languages = [
            os.path.basename(f).split(".")[0]
            for f in glob.glob(os.path.join(languages_dir, "*.json"))
        ]
        self.language_combo.addItems(languages)
        self.language_combo.setCurrentText(
            self.config.get("Settings", "language", fallback="english")
        )
        self.language_combo.currentIndexChanged.connect(self.change_language)
        toolbar.addWidget(self.language_combo)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        self.theme_combo.setCurrentText(self.theme)
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        toolbar.addWidget(self.theme_combo)

        save_button = QPushButton(self.lang.get("save_settings", "Save"))
        save_button.clicked.connect(self.save_settings)
        toolbar.addWidget(save_button)

    def create_ui(self):
        tabs = QTabWidget()
        # Main tab
        main_tab = QWidget()
        main_layout = QVBoxLayout(main_tab)

        title = QLabel(self.lang.get("title", "Temp File Deleter"))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px;")
        main_layout.addWidget(title)

        desc = QLabel(self.lang.get("description", "Remove temporary files."))
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("font-size: 12px; color: gray;")
        self.layout.addWidget(desc)

        self.checkboxes = {}
        drive_sections = {
            "d_drive": ["d_ame", "d_extensions"],
            "c_drive": ["c_ame", "c_extensions"],
        }

        for drive, children in drive_sections.items():
            section_label = QLabel(self.lang.get(drive, drive))
            section_label.setStyleSheet(
                "font-size: 16px; font-weight: bold; margin-top: 10px;"
            )
            self.layout.addWidget(section_label)

            for key in children:
                label = self.lang.get(key, key).replace("{username}", self.username)
                cb = QCheckBox(label)
                self.checkboxes[key] = cb
                self.layout.addWidget(cb)

        # Adobe cache as a special item
        label = self.lang.get("adobe_cache", "Adobe Cache").replace(
            "{username}", self.username
        )
        cb = QCheckBox(label)
        self.checkboxes["adobe_cache"] = cb
        self.layout.addWidget(cb)

        btn_layout = QHBoxLayout()
        self.delete_btn = QPushButton(self.lang.get("delete_files", "Delete Files"))
        self.delete_btn.clicked.connect(lambda: self.start_deletion(shutdown=False))
        btn_layout.addWidget(self.delete_btn)

        self.delete_shutdown_btn = QPushButton(self.lang["delete_files_shutdown"])
        self.delete_shutdown_btn.clicked.connect(
            lambda: self.start_deletion(shutdown=True)
        )
        btn_layout.addWidget(self.delete_shutdown_btn)
        main_layout.addLayout(btn_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        self.progress_bar = QProgressBar()
        main_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        main_layout.addWidget(self.status_label)

        tabs.addTab(main_tab, self.lang.get("main_tab", "Main"))

        # Advanced Options tab
        adv_tab = QWidget()
        adv_layout = QVBoxLayout(adv_tab)

        adv_desc = QLabel(self.lang.get("advanced_description", "Advanced: select specific paths to remove"))
        adv_desc.setStyleSheet("font-size: 12px; color: gray;")
        adv_layout.addWidget(adv_desc)

        # Advanced checkboxes for the three specific paths
        self.adv_checkboxes = {}
        # Temp folder
        cb_temp = QCheckBox(self.lang.get("temp_label", "C:\\Users\\{username}\\AppData\\Local\\Temp\\").replace("{username}", self.username))
        # set default from settings.ini (fallback True)
        cb_temp.setChecked(self.config.getboolean("Settings", "adv_temp", fallback=True))
        cb_temp.stateChanged.connect(lambda st, k="temp": self.on_adv_checkbox_changed(k, st))
        self.adv_checkboxes["temp"] = cb_temp
        adv_layout.addWidget(cb_temp)
        # After Effects (all versions)
        cb_ae = QCheckBox(self.lang.get("after_effects_label", "C:\\Users\\{username}\\AppData\\Local\\Temp\\Adobe\\After Effects\\").replace("{username}", self.username))
        cb_ae.setChecked(self.config.getboolean("Settings", "adv_after_effects", fallback=True))
        cb_ae.stateChanged.connect(lambda st, k="after_effects": self.on_adv_checkbox_changed(k, st))
        self.adv_checkboxes["after_effects"] = cb_ae
        adv_layout.addWidget(cb_ae)
        # Media Cache Files
        cb_media = QCheckBox(self.lang.get("media_cache_label", "C:\\Users\\{username}\\AppData\\Roaming\\Adobe\\Common\\Media Cache Files").replace("{username}", self.username))
        cb_media.setChecked(self.config.getboolean("Settings", "adv_media_cache", fallback=True))
        cb_media.stateChanged.connect(lambda st, k="media_cache": self.on_adv_checkbox_changed(k, st))
        self.adv_checkboxes["media_cache"] = cb_media
        adv_layout.addWidget(cb_media)

        tabs.addTab(adv_tab, self.lang.get("advanced_tab", "Advanced Options"))

        self.layout.addWidget(tabs)

    def on_adv_checkbox_changed(self, key, state):
        """Guardar el cambio inmediato en settings.ini (adv_<key> = true/false)."""
        checked = bool(state == Qt.CheckState.Checked or state == 2)
        # garantizar que la sección exista y escribir
        self.config.read(self.config_file)
        if "Settings" not in self.config:
            self.config["Settings"] = {}
        self.config["Settings"][f"adv_{key}"] = "true" if checked else "false"
        with open(self.config_file, "w", encoding="utf-8") as configfile:
            self.config.write(configfile)

    def change_language(self):
        self.config["Settings"] = {"language": self.language_combo.currentText()}
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)
        QMessageBox.information(
            self, "Language", "Language changed! Please restart the app to apply."
        )

    def change_theme(self):
        self.theme = self.theme_combo.currentText()
        self.apply_theme()

    def apply_theme(self):
        theme_file = os.path.join(
            os.path.dirname(__file__), "styles", f"{self.theme}_theme.qss"
        )
        with open(theme_file, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def save_settings(self):
        self.config["Settings"] = {
            "language": self.language_combo.currentText(),
            "theme": self.theme_combo.currentText(),
        }
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)
        QMessageBox.information(self, "Settings", "Settings saved!")

    def check_adobe_processes(self):
        """Check for running Adobe processes"""
        adobe_processes = []
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if any(name.lower() in proc.info['name'].lower() for name in [
                    'adobe', 'afterfx', 'photoshop', 'creative cloud'
                ]):
                    adobe_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return adobe_processes

    def kill_adobe_processes(self, processes):
        """Kill the specified Adobe processes"""
        for proc in processes:
            try:
                psutil.Process(proc['pid']).kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def start_deletion(self, shutdown=False):
        # Check for Adobe processes before starting
        adobe_processes = self.check_adobe_processes()
        if adobe_processes:
            process_names = ", ".join(proc['name'] for proc in adobe_processes)
            reply = QMessageBox.question(
                self,
                self.lang.get("adobe_running_title", "Adobe Processes Running"),
                self.lang.get("adobe_running_text", "The following Adobe processes are running:\n{processes}\n\nWould you like to close them and continue?").format(processes=process_names),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.kill_adobe_processes(adobe_processes)
            else:
                return

        self.progress_bar.setValue(0)
        threading.Thread(
            target=self.delete_files, args=(shutdown,), daemon=True
        ).start()

    def delete_files(self, shutdown=False):
        selected_tasks = [
            key for key, checkbox in self.checkboxes.items() if checkbox.isChecked()
        ]

        if not selected_tasks:
            QMetaObject.invokeMethod(
                self, "show_no_tasks_popup", Qt.ConnectionType.QueuedConnection
            )
            return

        progress_increment = 100 // len(selected_tasks)
        current_progress = 0

        for task in selected_tasks:
            # Add path info to status label
            path = self.get_path_for_task(task)
            QMetaObject.invokeMethod(
                self.status_label,
                "setText",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, self.lang.get("searching_in", "Searching in: {path}").format(path=path)),
            )
            
            if not path or not os.path.exists(path):
                continue
            filter_func = self.get_filter(task)
            # Process all files and folders in reverse order (bottom-up)
            for root, subdirs, files in os.walk(path, topdown=False):
                # First handle files in current directory
                for name in files:
                    if filter_func(name, False):
                        try:
                            file_path = os.path.join(root, name)
                            # Get file size before deletion
                            try:
                                self.space_cleared += os.path.getsize(file_path)
                                os.remove(file_path)
                                self.files_deleted += 1
                            except FileNotFoundError:
                                pass
                        except (PermissionError, OSError):
                            pass
                # Then handle subdirectories
                for name in subdirs:
                    if filter_func(name, True):
                        try:
                            full_subdir = os.path.join(root, name)
                            # No need to calculate folder size as we already counted its files
                            shutil.rmtree(full_subdir, ignore_errors=True)
                            self.folders_deleted += 1
                        except (PermissionError, OSError):
                            pass
            current_progress += progress_increment
            QMetaObject.invokeMethod(
                self.progress_bar,
                "setValue",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(int, current_progress),
            )

        QMetaObject.invokeMethod(
            self.progress_bar,
            "setValue",
            Qt.ConnectionType.QueuedConnection,
            Q_ARG(int, 100),
        )
        QMetaObject.invokeMethod(
            self.status_label,
            "setText",
            Qt.ConnectionType.QueuedConnection,
            Q_ARG(str, self.lang.get("operation_completed", "Operation completed.")),
        )
        QMetaObject.invokeMethod(self, "show_popup", Qt.ConnectionType.QueuedConnection)

        if shutdown:
            os.system("shutdown /s /t 0")

    def get_path_for_task(self, task):
        """Helper method to get the root path for a task"""
        paths = {
            "d_ame": "D:/",
            "d_extensions": "D:/",
            "c_ame": "C:/",
            "c_extensions": "C:/",
            "adobe_cache": f"C:/Users/{self.username}/AppData/Roaming/Adobe/common/Media Cache Files",
        }
        return paths.get(task)

    def get_filter(self, task):
        """Get the filter function for what to delete in the task"""
        if task == "adobe_cache":
            return lambda name, is_dir: True
        elif task in ["d_ame", "c_ame"]:
            return lambda name, is_dir: "_AME" in name
        elif task == "d_extensions":
            exts = [".mpgindex", ".ims", ".cfa", ".pek"]
            return lambda name, is_dir: not is_dir and any(name.endswith(ext) for ext in exts)
        elif task == "c_extensions":
            exts = [".mpgindex", ".ims", ".cfa", ".pek"]
            return lambda name, is_dir: not is_dir and any(name.endswith(ext) for ext in exts)
        return lambda name, is_dir: False

    @pyqtSlot()
    def show_no_tasks_popup(self):
        QMessageBox.warning(
            self,
            self.lang.get("advisory", "Warning"),
            self.lang.get(
                "no_tasks_selected",
                "No tasks were selected. Please select at least one task to proceed.",
            ),
        )

    @pyqtSlot()
    def show_popup(self):
        QMessageBox.information(
            self,
            self.lang.get("operation_completed", "Operation completed"),
            self.lang.get("files_deleted_success", "Files deleted successfully!"),
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TempFileDeleter()
    window.apply_theme()
    window.show()
    sys.exit(app.exec())

