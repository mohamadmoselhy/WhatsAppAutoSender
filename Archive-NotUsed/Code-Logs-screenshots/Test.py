import time
import os

ONEDRIVE_PATH = os.path.expanduser("~/OneDrive - Giza Systems")  # Adjust this path

def get_all_files():
    try:
        file_paths = set()
        for root, _, files in os.walk(ONEDRIVE_PATH):
            for file in files:
                file_paths.add(os.path.join(root, file))
        return file_paths
    except Exception as e:
        print(f"Error while scanning files: {e}")
        raise

previous_files = get_all_files()

while True:
    try:
        time.sleep(5)  # Check every 5 seconds
        current_files = get_all_files()
        new_files = current_files - previous_files
        
        if new_files:
            for file in new_files:
                print(f"New file detected: {file}")
        
        previous_files = current_files
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
