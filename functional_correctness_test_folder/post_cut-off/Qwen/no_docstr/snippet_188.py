
import os
import time
import threading
from datetime import datetime, timedelta


class LogCleanupManager:

    def __init__(self, log_dir: str, max_age_days: int = 30, cleanup_interval_hours: int = 24):
        self.log_dir = log_dir
        self.max_age_days = max_age_days
        self.cleanup_interval_hours = cleanup_interval_hours
        self.cleanup_thread = None
        self.cleanup_stats = {'files_deleted': 0, 'errors': 0}
        self._stop_event = threading.Event()

    def start_cleanup_scheduler(self):
        if self.cleanup_thread is None:
            self._stop_event.clear()
            self.cleanup_thread = threading.Thread(target=self._cleanup_loop)
            self.cleanup_thread.start()

    def stop_cleanup_scheduler(self):
        if self.cleanup_thread is not None:
            self._stop_event.set()
            self.cleanup_thread.join()
            self.cleanup_thread = None

    def _cleanup_loop(self):
        while not self._stop_event.is_set():
            self.cleanup_old_logs()
            time.sleep(self.cleanup_interval_hours * 3600)

    def cleanup_old_logs(self):
        try:
            max_age = datetime.now() - timedelta(days=self.max_age_days)
            for filename in os.listdir(self.log_dir):
                file_path = os.path.join(self.log_dir, filename)
                if os.path.isfile(file_path):
                    file_modified_time = datetime.fromtimestamp(
                        os.path.getmtime(file_path))
                    if file_modified_time < max_age:
                        os.remove(file_path)
                        self.cleanup_stats['files_deleted'] += 1
        except Exception as e:
            self.cleanup_stats['errors'] += 1
            print(f"Error during log cleanup: {e}")

    def get_cleanup_stats(self) -> dict:
        return self.cleanup_stats.copy()
