
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
        self.stop_event = threading.Event()
        self.cleanup_stats = {
            'last_cleanup_time': None,
            'total_logs': 0,
            'deleted_logs': 0,
            'remaining_logs': 0
        }

    def start_cleanup_scheduler(self):
        self.stop_event.clear()
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop)
        self.cleanup_thread.start()

    def stop_cleanup_scheduler(self):
        self.stop_event.set()
        if self.cleanup_thread is not None:
            self.cleanup_thread.join()

    def _cleanup_loop(self):
        while not self.stop_event.is_set():
            self.cleanup_old_logs()
            time.sleep(self.cleanup_interval_hours * 3600)

    def cleanup_old_logs(self):
        now = datetime.now()
        cutoff_time = now - timedelta(days=self.max_age_days)
        deleted_logs = 0

        for filename in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, filename)
            if os.path.isfile(file_path):
                file_mtime = datetime.fromtimestamp(
                    os.path.getmtime(file_path))
                if file_mtime < cutoff_time:
                    os.remove(file_path)
                    deleted_logs += 1

        self.cleanup_stats['last_cleanup_time'] = now
        self.cleanup_stats['total_logs'] = len(os.listdir(self.log_dir))
        self.cleanup_stats['deleted_logs'] = deleted_logs
        self.cleanup_stats['remaining_logs'] = self.cleanup_stats['total_logs'] - deleted_logs

    def get_cleanup_stats(self) -> dict:
        return self.cleanup_stats
