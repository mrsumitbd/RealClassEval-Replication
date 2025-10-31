
import os
import threading
import time
from datetime import datetime, timedelta


class LogCleanupManager:

    def __init__(self, log_dir: str, max_age_days: int = 30, cleanup_interval_hours: int = 24):
        '''
        Initialize log cleanup manager.
        Args:
            log_dir: Directory containing log files
            max_age_days: Maximum age of log files in days (default: 30 days)
            cleanup_interval_hours: Cleanup interval in hours (default: 24 hours)
        '''
        self.log_dir = log_dir
        self.max_age_days = max_age_days
        self.cleanup_interval_hours = cleanup_interval_hours
        self._scheduler_thread = None
        self._stop_event = threading.Event()
        self._last_cleanup_time = None
        self._last_deleted_files = []
        self._last_cleanup_count = 0

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        if self._scheduler_thread and self._scheduler_thread.is_alive():
            return  # Already running
        self._stop_event.clear()
        self._scheduler_thread = threading.Thread(
            target=self._cleanup_loop, daemon=True)
        self._scheduler_thread.start()

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        self._stop_event.set()
        if self._scheduler_thread:
            self._scheduler_thread.join()
            self._scheduler_thread = None

    def _cleanup_loop(self):
        while not self._stop_event.is_set():
            self.cleanup_old_logs()
            # Wait for the interval or until stop event is set
            for _ in range(int(self.cleanup_interval_hours * 60 * 60)):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        now = time.time()
        cutoff = now - self.max_age_days * 86400
        deleted_files = []
        count = 0
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
                        count += 1
                except Exception:
                    continue
        self._last_cleanup_time = datetime.now()
        self._last_deleted_files = deleted_files
        self._last_cleanup_count = count

    def get_cleanup_stats(self) -> dict:
        '''Get statistics about log files and cleanup status'''
        total_files = 0
        total_size = 0
        if os.path.isdir(self.log_dir):
            for filename in os.listdir(self.log_dir):
                file_path = os.path.join(self.log_dir, filename)
                if os.path.isfile(file_path):
                    total_files += 1
                    try:
                        total_size += os.path.getsize(file_path)
                    except Exception:
                        continue
        stats = {
            'log_dir': self.log_dir,
            'total_files': total_files,
            'total_size_bytes': total_size,
            'last_cleanup_time': self._last_cleanup_time,
            'last_deleted_files': self._last_deleted_files,
            'last_cleanup_count': self._last_cleanup_count,
        }
        return stats
