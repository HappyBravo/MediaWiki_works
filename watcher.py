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
    print("Watcher Started")
    
    # REQUIRED INFO FOR LOGIN AND FILE PATH
    # Provide the necessary information here
    username = "mediawiki_admin" # Replace with your username
    password = "mediawiki@123"   # replace with your password
    path = "./PDFs"              # Replace with the directory you want to monitor

    sleep_time =  3              # in seconds, for waiting
    errorr = False

    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
   
    try:
        while True and not errorr:
            errorr = False
            time.sleep(sleep_time)  # Wait for some time
            if event_handler.new_files:
                print("New files detected. Performing task...")

                # Create the "temp_PDFs" directory
                pdfs_dir = os.path.join(path, "temp_PDFs")
                os.makedirs(pdfs_dir, exist_ok=True)

                # Copy new files to "temp_PDFs" directory for temporary storage and processing
                for file_path in event_handler.new_files:
                    if file_path.endswith('.part'):
                        file_path = file_path[:-5]   # REMOVING THE ".part" extension # Perform your task here (e.g., "upload")
                    shutil.copy2(file_path, pdfs_dir)

                # Create "new" folder. It will be used by MW_pybot for storing the processed PDFs
                new_dir = os.path.join(pdfs_dir, "new") 
                os.makedirs(new_dir, exist_ok=True)
                
                # Performing operations on the files in "temp_PDFs"
                try:
                    uploader.main_uploader(file_path=pdfs_dir, username=username, password = password)
                    
                    # Clear the list of new files
                    event_handler.new_files = []
                    print("Task completed successfully.")

                except Exception as e:
                    # errorr = True
                    print(e)
                    
                
                # Delete the "PDFs" directory and its contents
                shutil.rmtree(pdfs_dir)
                if errorr:
                    print("error detected ... ")
                    raise Exception
                    # break

            else:
                print("No new files detected. Skipping task.")
    except KeyboardInterrupt:
    # except Exception as e:
        print("Interrupted ... Exiting")
        # print(e)
        observer.stop()

    observer.join()

