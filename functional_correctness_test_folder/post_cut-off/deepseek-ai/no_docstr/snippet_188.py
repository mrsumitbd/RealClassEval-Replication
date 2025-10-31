
import os
import time
import threading
from datetime import datetime, timedelta


class LogCleanupManager:

    def __init__(self, log_dir: str, max_age_days: int = 30, cleanup_interval_hours: int = 24):
        self.log_dir = log_dir
        self.max_age_days = max_age_days
        self.cleanup_interval_hours = cleanup_interval_hours
        self._scheduler_thread = None
        self._stop_event = threading.Event()
        self._cleanup_stats = {
            'total_deleted': 0,
            'last_cleanup_time': None,
            'last_deleted_count': 0
        }

    def start_cleanup_scheduler(self):
        if self._scheduler_thread is not None and self._scheduler_thread.is_alive():
            return
        self._stop_event.clear()
        self._scheduler_thread = threading.Thread(
            target=self._cleanup_loop, daemon=True)
        self._scheduler_thread.start()

    def stop_cleanup_scheduler(self):
        self._stop_event.set()
        if self._scheduler_thread is not None:
            self._scheduler_thread.join()

    def _cleanup_loop(self):
        while not self._stop_event.is_set():
            self.cleanup_old_logs()
            time.sleep(self.cleanup_interval_hours * 3600)

    def cleanup_old_logs(self):
        if not os.path.exists(self.log_dir):
            return
        now = datetime.now()
        cutoff_time = now - timedelta(days=self.max_age_days)
        deleted_count = 0

        for filename in os.listdir(self.log_dir):
            filepath = os.path.join(self.log_dir, filename)
            if os.path.isfile(filepath):
                file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if file_mtime < cutoff_time:
                    try:
                        os.remove(filepath)
                        deleted_count += 1
                    except OSError:
                        continue

        self._cleanup_stats['total_deleted'] += deleted_count
        self._cleanup_stats['last_deleted_count'] = deleted_count
        self._cleanup_stats['last_cleanup_time'] = now

    def get_cleanup_stats(self) -> dict:
        return self._cleanup_stats.copy()
