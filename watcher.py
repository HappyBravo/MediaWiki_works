import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import MW_pybot as uploader

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.new_files = []

    def on_created(self, event):
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            self.new_files.append(event.src_path)

if __name__ == "__main__":
    path = "./PDFs"  # Replace with the directory you want to monitor
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    username = "mediawiki_admin"
    sleep_time = 180 # in seconds

    try:
        while True:
            time.sleep(sleep_time)  # Wait for 30 minutes
            if event_handler.new_files:
                print("New files detected. Performing task...")
                # Perform your task here (e.g., "upload")

                # Create the "PDFs" directory
                pdfs_dir = os.path.join(path, "temp_PDFs")
                os.makedirs(pdfs_dir, exist_ok=True)

                # Copy new files to "PDFs" directory
                for file_path in event_handler.new_files:
                    if file_path.endswith('.part'):
                        file_path = file_path[:-5]
                    shutil.copy2(file_path, pdfs_dir)
                
                new_dir = os.path.join(pdfs_dir, "new")
                os.makedirs(new_dir, exist_ok=True)
                
                # Performing operations on the files in "PDFs"
                try:
                    uploader.main_uploader(file_path=pdfs_dir, username=username)
                    
                    # Clear the list of new files
                    event_handler.new_files = []
                    print("Task completed successfully.")
    
                except Exception as e:
                    print(e)
                
                # Delete the "PDFs" directory and its contents
                shutil.rmtree(pdfs_dir)

            else:
                print("No new files detected. Skipping task.")
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

