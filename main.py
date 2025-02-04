import tkinter as tk
from tkinter import ttk
import os
import shutil
import threading

class TempFileDeleter:
    def __init__(self, window):
        self.window = window
        self.username = os.environ.get("USERNAME")
        self.files_deleted = 0
        self.folders_deleted = 0
        self.setup_ui()
        self.toggle_checkboxes()

    def setup_ui(self):
        self.window.geometry("850x500")
        name = tk.Label(self.window, text="Kill Temp All", font=("Helvetica", 20))
        name.pack(padx=10, pady=1)
        desc = tk.Label(self.window, text="A simple program to delete all Adobe temporary files", font=("Helvetica", 10))
        desc.pack(padx=10, pady=1)
        self.create_checkboxes()
        self.create_buttons()
        self.create_advisory_label()

    def create_checkboxes(self):
        self.checkbox_frame = tk.Frame(self.window)
        self.checkbox_frame.pack(padx=10, pady=10)
        self.path_vars = []

        self.d_drive_var, self.d_drive_checkbox = self.create_checkbox(self.checkbox_frame, "D:/", padx=10)
        self.d_ame_var, self.d_ame_checkbox = self.create_checkbox(self.checkbox_frame, "_AME folders", padx=30)
        self.d_extensions_var, self.d_extensions_checkbox = self.create_checkbox(self.checkbox_frame, ".mpgindex, .ims, .cfa, .pek file extensions", padx=30)

        self.c_drive_var, self.c_drive_checkbox = self.create_checkbox(self.checkbox_frame, "C:/", padx=10)
        self.c_ame_var, self.c_ame_checkbox = self.create_checkbox(self.checkbox_frame, "_AME folders", padx=30)
        self.c_extensions_var, self.c_extensions_checkbox = self.create_checkbox(self.checkbox_frame, ".mpgindex, .ims, .cfa, .pek file extensions", padx=30)

        self.e_drive_var = self.create_checkbox(self.checkbox_frame, "E:/", padx=10)[0]
        self.adobe_cache_var = self.create_checkbox(self.checkbox_frame, f"C:/Users/{self.username}/AppData/Roaming/Adobe/common/Media Cache Files", padx=10)[0]

        self.d_drive_var.trace_add('write', lambda *args: self.toggle_suboptions(self.d_drive_var, [(self.d_ame_var, self.d_ame_checkbox), (self.d_extensions_var, self.d_extensions_checkbox)]))
        self.c_drive_var.trace_add('write', lambda *args: self.toggle_suboptions(self.c_drive_var, [(self.c_ame_var, self.c_ame_checkbox), (self.c_extensions_var, self.c_extensions_checkbox)]))

    def create_buttons(self):
        self.btn_frame = tk.Frame(self.window)
        self.btn_frame.pack(padx=10, pady=10)
        self.btn = tk.Button(self.btn_frame, text="Delete temporary files", command=lambda: self.start_deletion(shutdown=False))
        self.btn.pack(side=tk.LEFT, padx=5)
        self.btn2 = tk.Button(self.btn_frame, text="Delete temporary files & shut down the computer", command=lambda: self.start_deletion(shutdown=True))
        self.btn2.pack(side=tk.LEFT, padx=5)

    def create_advisory_label(self):
        advisory = tk.Label(self.window, text="Select the paths you want to delete. Be careful, some folders may be used by Adobe, and you might not want to delete certain files/folders.", font=("Helvetica", 10))
        advisory.pack(padx=10, pady=1)

    def create_checkbox(self, parent, text, padx=20):
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(parent, text=text, variable=var)
        checkbox.pack(anchor='w', padx=padx)
        self.path_vars.append(var)
        return var, checkbox

    def toggle_suboptions(self, main_var, sub_vars):
        state = tk.NORMAL if main_var.get() else tk.DISABLED
        for var in sub_vars:
            var[1].config(state=state)

    def start_deletion(self, shutdown=False):
        self.btn.config(state=tk.DISABLED)
        self.btn2.config(state=tk.DISABLED)
        self.progress_bar = ttk.Progressbar(self.window, mode='indeterminate')
        self.progress_bar.pack(padx=10, pady=10, fill=tk.X)
        self.separator = ttk.Separator(self.window, orient='horizontal')
        self.separator.pack(fill='x', padx=10, pady=10)
        labels_frame = tk.Frame(self.window)
        labels_frame.pack(padx=10, pady=1)
        self.label_folders = tk.Label(labels_frame, text=f"Folders deleted: {self.folders_deleted}", bg="yellow")
        self.label_folders.pack(side=tk.LEFT, padx=5)
        self.label_files = tk.Label(labels_frame, text=f"Files deleted: {self.files_deleted}", bg="red")
        self.label_files.pack(side=tk.LEFT, padx=5)
        self.label_completed = tk.Label(labels_frame, text="")
        self.label_completed.pack(side=tk.LEFT, padx=5)
        threading.Thread(target=self.delete_files, args=(shutdown,)).start()

    def delete_files(self, shutdown=False):
        print("Deleting temporary files...")
        self.progress_bar.start()
        paths = [
            ("D:/", "_AME", self.d_ame_var), ("C:/", "_AME", self.c_ame_var),
            ("D:/", [".mpgindex", ".ims", ".cfa", ".pek"], self.d_extensions_var),
            ("C:/", [".mpgindex", ".ims", ".cfa", ".pek"], self.c_extensions_var),
            ("E:/", None, self.e_drive_var),
            (f"C:/Users/{self.username}/AppData/Roaming/Adobe/common/Media Cache Files", None, self.adobe_cache_var)
        ]
        paths = [(path, condition) for path, condition, var in paths if var.get()]
        for path, condition in paths:
            self.label_completed.config(text=f"Searching in {path}...", bg="orange")
            self.delete_path(path, condition)
            self.window.update_idletasks()
        print("Files deleted")
        self.progress_bar.stop()
        self.progress_bar.config(value=100)
        self.label_completed.config(text="Operation completed", bg="green", width=30)
        if shutdown:
            print("Shutting down the computer...")
            os.system("shutdown /s /t 1")

    def delete_path(self, path, condition=None):
        for root, subdirs, files in os.walk(path, topdown=False):
            if condition is None:
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                        self.files_deleted += 1
                        self.label_files.config(text=f"Files deleted: {self.files_deleted}")
                    except PermissionError:
                        pass
                for name in subdirs:
                    try:
                        shutil.rmtree(os.path.join(root, name))
                        self.folders_deleted += 1
                        self.label_folders.config(text=f"Folders deleted: {self.folders_deleted}")
                    except PermissionError:
                        pass
            elif isinstance(condition, str):
                for name in subdirs:
                    if name.endswith(condition):
                        try:
                            shutil.rmtree(os.path.join(root, name))
                            self.folders_deleted += 1
                            self.label_folders.config(text=f"Folders deleted: {self.folders_deleted}")
                        except PermissionError:
                            pass
            elif isinstance(condition, list):
                for name in files:
                    if any(name.endswith(ext) for ext in condition):
                        try:
                            os.remove(os.path.join(root, name))
                            self.files_deleted += 1
                            self.label_files.config(text=f"Files deleted: {self.files_deleted}")
                        except PermissionError:
                            pass

    def toggle_checkboxes(self):
        self.d_drive_var.set(True)
        self.d_drive_var.set(False)
        self.c_drive_var.set(True)
        self.c_drive_var.set(False)

if __name__ == "__main__":
    window = tk.Tk()
    app = TempFileDeleter(window)
    window.mainloop()