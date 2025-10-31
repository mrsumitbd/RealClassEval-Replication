import os
import threading
import time
from datetime import datetime, timedelta


class LogCleanupManager:
    '''Log file cleanup manager for automatic maintenance'''

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
        self._last_cleanup_deleted = 0
        self._last_cleanup_files = 0
        self._lock = threading.Lock()

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        if self._scheduler_thread and self._scheduler_thread.is_alive():
            return
        self._stop_event.clear()
        self._scheduler_thread = threading.Thread(
            target=self._cleanup_loop, daemon=True)
        self._scheduler_thread.start()

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        self._stop_event.set()
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)

    def _cleanup_loop(self):
        '''Background loop for periodic cleanup'''
        while not self._stop_event.is_set():
            self.cleanup_old_logs()
            for _ in range(int(self.cleanup_interval_hours * 60 * 60)):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        now = time.time()
        cutoff = now - self.max_age_days * 86400
        deleted = 0
        total_files = 0
        with self._lock:
            if not os.path.isdir(self.log_dir):
                self._last_cleanup_time = datetime.now()
                self._last_cleanup_deleted = 0
                self._last_cleanup_files = 0
                return
            for fname in os.listdir(self.log_dir):
                fpath = os.path.join(self.log_dir, fname)
                if not os.path.isfile(fpath):
                    continue
                total_files += 1
                try:
                    mtime = os.path.getmtime(fpath)
                    if mtime < cutoff:
                        os.remove(fpath)
                        deleted += 1
                except Exception:
                    continue
            self._last_cleanup_time = datetime.now()
            self._last_cleanup_deleted = deleted
            self._last_cleanup_files = total_files

    def get_cleanup_stats(self) -> dict:
        '''Get statistics about log files and cleanup status'''
        with self._lock:
            stats = {
                'log_dir': self.log_dir,
                'max_age_days': self.max_age_days,
                'cleanup_interval_hours': self.cleanup_interval_hours,
                'last_cleanup_time': self._last_cleanup_time.isoformat() if self._last_cleanup_time else None,
                'last_cleanup_deleted': self._last_cleanup_deleted,
                'last_cleanup_files': self._last_cleanup_files,
                'current_log_files': 0,
            }
            try:
                if os.path.isdir(self.log_dir):
                    stats['current_log_files'] = len([
                        f for f in os.listdir(self.log_dir)
                        if os.path.isfile(os.path.join(self.log_dir, f))
                    ])
            except Exception:
                stats['current_log_files'] = None
            return stats
