
import os
import time
import threading
from datetime import datetime, timedelta


class LogCleanupManager:

    def __init__(self, log_dir: str, max_age_days: int = 30, cleanup_interval_hours: int = 24):
        self.log_dir = log_dir
        self.max_age_days = max_age_days
        self.cleanup_interval_hours = cleanup_interval_hours
        self.scheduler_thread = None
        self.cleanup_stats = {'files_deleted': 0, 'files_checked': 0}
        self._stop_event = threading.Event()

    def start_cleanup_scheduler(self):
        if self.scheduler_thread is None or not self.scheduler_thread.is_alive():
            self._stop_event.clear()
            self.scheduler_thread = threading.Thread(target=self._cleanup_loop)
            self.scheduler_thread.start()

    def stop_cleanup_scheduler(self):
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self._stop_event.set()
            self.scheduler_thread.join()
            self.scheduler_thread = None

    def _cleanup_loop(self):
        while not self._stop_event.is_set():
            self.cleanup_old_logs()
            time.sleep(self.cleanup_interval_hours * 3600)

    def cleanup_old_logs(self):
        max_age = timedelta(days=self.max_age_days)
        current_time = datetime.now()
        for filename in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, filename)
            if os.path.isfile(file_path):
                self.cleanup_stats['files_checked'] += 1
                file_modified_time = datetime.fromtimestamp(
                    os.path.getmtime(file_path))
                if current_time - file_modified_time > max_age:
                    os.remove(file_path)
                    self.cleanup_stats['files_deleted'] += 1

    def get_cleanup_stats(self) -> dict:
        return self.cleanup_stats.copy()
