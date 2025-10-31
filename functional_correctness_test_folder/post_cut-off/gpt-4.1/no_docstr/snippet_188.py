
import os
import threading
import time
from datetime import datetime, timedelta


class LogCleanupManager:

    def __init__(self, log_dir: str, max_age_days: int = 30, cleanup_interval_hours: int = 24):
        self.log_dir = log_dir
        self.max_age_days = max_age_days
        self.cleanup_interval_hours = cleanup_interval_hours
        self._scheduler_thread = None
        self._stop_event = threading.Event()
        self._stats = {
            'last_cleanup': None,
            'files_deleted': 0,
            'last_deleted_files': [],
        }
        self._lock = threading.Lock()

    def start_cleanup_scheduler(self):
        if self._scheduler_thread and self._scheduler_thread.is_alive():
            return
        self._stop_event.clear()
        self._scheduler_thread = threading.Thread(
            target=self._cleanup_loop, daemon=True)
        self._scheduler_thread.start()

    def stop_cleanup_scheduler(self):
        self._stop_event.set()
        if self._scheduler_thread:
            self._scheduler_thread.join()
            self._scheduler_thread = None

    def _cleanup_loop(self):
        while not self._stop_event.is_set():
            self.cleanup_old_logs()
            for _ in range(int(self.cleanup_interval_hours * 60 * 60)):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

    def cleanup_old_logs(self):
        now = time.time()
        cutoff = now - self.max_age_days * 86400
        deleted_files = []
        if not os.path.isdir(self.log_dir):
            return
        for filename in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, filename)
            if os.path.isfile(file_path):
                try:
                    mtime = os.path.getmtime(file_path)
                    if mtime < cutoff:
                        os.remove(file_path)
                        deleted_files.append(filename)
                except Exception:
                    continue
        with self._lock:
            self._stats['last_cleanup'] = datetime.now()
            self._stats['files_deleted'] += len(deleted_files)
            self._stats['last_deleted_files'] = deleted_files

    def get_cleanup_stats(self) -> dict:
        with self._lock:
            return dict(self._stats)
