import os
import random
import string
import time
from pathlib import Path

def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_random_file(path, min_size=1024, max_size=1024*1024):
    """Create a file with random content and size between min_size and max_size bytes"""
    size = random.randint(min_size, max_size)
    with open(path, 'wb') as f:
        f.write(os.urandom(size))
    return size

def create_test_files():
    username = os.environ.get("USERNAME") or os.environ.get("USER")
    
    # Define paths
    paths = {
        "Temp": Path(f"C:/Users/{username}/AppData/Local/Temp"),
        "After Effects": Path(f"C:/Users/{username}/AppData/Local/Temp/Adobe/After Effects"),
        "Media Cache": Path(f"C:/Users/{username}/AppData/Roaming/Adobe/Common/Media Cache Files")
    }
    
    # Common temp file extensions
    ae_extensions = ['.tmp', '.aep', '.aet', '.mp4', '.mov', '.mpgindex', '.ims', '.cfa', '.pek']
    temp_extensions = ['.tmp', '.temp', '.log', '.old', '.bak']
    cache_extensions = ['.mcf', '.mcl', '.mcs', '.pek', '.cfa']
    
    total_files = 0
    total_folders = 0
    total_size = 0
    
    print("Creating test files...")
    
    for name, path in paths.items():
        # Create base directory if it doesn't exist
        path.mkdir(parents=True, exist_ok=True)
        
        # Create random subdirectories
        num_dirs = random.randint(3, 8)
        for _ in range(num_dirs):
            subdir = path / f"test_{random_string(8)}"
            subdir.mkdir(exist_ok=True)
            total_folders += 1
            
            # Files per directory
            num_files = random.randint(5, 15)
            
            # Select appropriate extensions for this path
            if "After Effects" in str(path):
                extensions = ae_extensions
            elif "Media Cache" in str(path):
                extensions = cache_extensions
            else:
                extensions = temp_extensions
            
            # Create random files
            for _ in range(num_files):
                ext = random.choice(extensions)
                filename = f"test_{random_string(12)}{ext}"
                file_path = subdir / filename
                
                size = create_random_file(file_path)
                total_size += size
                total_files += 1
                
                # Simulate file creation time difference
                access_time = time.time() - random.randint(0, 60*60*24*30)  # Up to 30 days old
                os.utime(file_path, (access_time, access_time))

    print(f"\nCreated test environment:")
    print(f"- Total folders: {total_folders}")
    print(f"- Total files: {total_files}")
    print(f"- Total size: {total_size / (1024*1024):.2f} MB")
    print("\nPaths created:")
    for name, path in paths.items():
        print(f"- {name}: {path}")

if __name__ == "__main__":
    create_test_files()
