import time
import subprocess
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the UiPath Process Name (Change this to match your process in UiPath Assistant)
UIPATH_PROCESS_NAME = "Archive/DOF"

class FileAddedHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:  # Ignore folder creation events
            print(f"New file added: {event.src_path}")
            self.start_uipath_process(event.src_path)  # ✅ Pass file path to UiPath process

    def start_uipath_process(self, file_path):
        try:
            # Change this path if UiRobot.exe is installed in a different location
            uipath_exe = r"C:\Users\Lenovo\AppData\Local\Programs\UiPath\Studio\UiRobot.exe"
            
            # Prepare input argument as JSON (UiPath requires JSON format)
            input_arg = json.dumps({"FilePath": file_path})  # UiPath should expect a "FilePath" argument
            
            # Run the UiPath process with the file path as input
            subprocess.run([uipath_exe, "execute", "--process", UIPATH_PROCESS_NAME, "--input", input_arg], check=True)
            
            print(f"✅ UiPath process '{UIPATH_PROCESS_NAME}' started successfully with file: {file_path}")
        
        except Exception as e:
            print(f"❌ Error starting UiPath process: {e}")

def monitor_folder(folder_path):
    event_handler = FileAddedHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)  # ✅ Recursively monitors all subfolders
    observer.start()
    
    try:
        while True:
            time.sleep(1)  # Keeps the script running
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

# Example: Set the folder path you want to monitor
folder_to_watch = r"D:\My drive\Course\Data Science\Projects\Mostql\Test Folder"  # Change this to your target folder
monitor_folder(folder_to_watch)
