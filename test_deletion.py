import os
import random
import string
from pathlib import Path

def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_random_file(path, min_size=1024, max_size=1024*1024):
    """Create a file with random content and size between min_size and max_size bytes"""
    size = random.randint(min_size, max_size)
    with open(path, 'wb') as f:
        f.write(os.urandom(size))
    return size

def create_test_files_for_deletion():
    username = os.environ.get("USERNAME") or os.environ.get("USER")
    
    # Paths for main deletion tasks
    test_paths = {
        "D:/temp_test": ["d_ame", "d_extensions"],
        "C:/temp_test": ["c_ame", "c_extensions"],
    }
    
    # Adobe cache path
    adobe_cache = Path(f"C:/Users/{username}/AppData/Roaming/Adobe/Common/Media Cache Files")
    adobe_cache.mkdir(parents=True, exist_ok=True)
    
    # Extensions to create for extensions task
    ext_files = ['.mpgindex', '.ims', '.cfa', '.pek']
    
    total_files = 0
    total_folders = 0
    total_size = 0
    
    print("Creating test files for deletion testing...")
    
    # For D:/ and C:/ tasks
    for drive, tasks in test_paths.items():
        drive_path = Path(drive)
        drive_path.mkdir(parents=True, exist_ok=True)
        if not drive_path.exists():
            print(f"Drive {drive} not found, skipping.")
            continue
        
        for task in tasks:
            if task.endswith("_ame"):
                # Create folders and files with "_AME" in name
                for i in range(3):
                    folder_name = f"test_AME_{random_string(5)}"
                    folder_path = drive_path / folder_name
                    folder_path.mkdir(exist_ok=True)
                    total_folders += 1
                    # Create some files in it
                    for j in range(2):
                        file_path = folder_path / f"file_{random_string(3)}.tmp"
                        size = create_random_file(file_path)
                        total_size += size
                        total_files += 1
            elif task.endswith("_extensions"):
                # Create files with specific extensions
                for ext in ext_files:
                    for i in range(2):
                        file_name = f"test_{random_string(5)}{ext}"
                        file_path = drive_path / file_name
                        size = create_random_file(file_path)
                        total_size += size
                        total_files += 1
    
    # For Adobe cache, create some files (though create_test_files.py might do this)
    for i in range(5):
        file_path = adobe_cache / f"cache_{random_string(8)}.mcf"
        size = create_random_file(file_path)
        total_size += size
        total_files += 1
    
    # Also create some files that should NOT be deleted
    safe_file = Path("D:/temp_test") / "safe_file.txt"
    with open(safe_file, 'w') as f:
        f.write("This file should not be deleted.")
    total_files += 1
    
    safe_folder = Path("D:/temp_test") / "safe_folder"
    safe_folder.mkdir(exist_ok=True)
    total_folders += 1
    
    print(f"Created {total_files} test files, {total_folders} test folders, total size: {total_size} bytes.")
    print("Run the main program to test deletion. The safe_file.txt and safe_folder should remain.")

if __name__ == "__main__":
    create_test_files_for_deletion()
