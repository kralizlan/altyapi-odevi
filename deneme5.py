import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIR = "/home/ubuntu/bsm/test"
LOG_FILE = "/home/ubuntu/bsm/logs/changes.json"

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self.log_event("modified", event.src_path)

    def on_created(self, event):
        self.log_event("created", event.src_path)

    def on_deleted(self, event):
        self.log_event("deleted", event.src_path)

    def log_event(self, event_type, file_path):
        event = {
            "event_type": event_type,
            "file_path": file_path,
            "timestamp": time.ctime()
        }
        try:
            with open(LOG_FILE, "a") as log_file:
                json.dump(event, log_file)
                log_file.write("\n")
        except Exception as e:
            print(f"Log yazma hatası: {e}")


if __name__ == "__main__":
    if not os.path.exists(WATCH_DIR):
        os.makedirs(WATCH_DIR)

    if not os.path.exists(os.path.dirname(LOG_FILE)):
        os.makedirs(os.path.dirname(LOG_FILE))

    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    observer.start()
    print(f"Monitoring directory: {WATCH_DIR}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

