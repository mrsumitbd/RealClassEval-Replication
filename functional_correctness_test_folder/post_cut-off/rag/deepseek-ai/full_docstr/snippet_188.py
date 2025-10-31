
import os
import time
import threading
from datetime import datetime, timedelta
from typing import Dict


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
        self._stop_event = threading.Event()
        self._cleanup_thread = None
        self._last_cleanup_time = None
        self._total_files_deleted = 0
        self._total_bytes_freed = 0

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        if self._cleanup_thread is not None and self._cleanup_thread.is_alive():
            return
        self._stop_event.clear()
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        self._stop_event.set()
        if self._cleanup_thread is not None:
            self._cleanup_thread.join()
            self._cleanup_thread = None

    def _cleanup_loop(self):
        '''Background loop for periodic cleanup'''
        while not self._stop_event.is_set():
            self.cleanup_old_logs()
            self._stop_event.wait(self.cleanup_interval_hours * 3600)

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        if not os.path.isdir(self.log_dir):
            return
        cutoff_time = datetime.now() - timedelta(days=self.max_age_days)
        files_deleted = 0
        bytes_freed = 0
        for filename in os.listdir(self.log_dir):
            filepath = os.path.join(self.log_dir, filename)
            if not os.path.isfile(filepath):
                continue
            file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if file_mtime < cutoff_time:
                try:
                    file_size = os.path.getsize(filepath)
                    os.remove(filepath)
                    files_deleted += 1
                    bytes_freed += file_size
                except OSError:
                    continue
        self._last_cleanup_time = datetime.now()
        self._total_files_deleted += files_deleted
        self._total_bytes_freed += bytes_freed

    def get_cleanup_stats(self) -> dict:
        '''Get statistics about log files and cleanup status'''
        stats = {
            'log_dir': self.log_dir,
            'max_age_days': self.max_age_days,
            'cleanup_interval_hours': self.cleanup_interval_hours,
            'last_cleanup_time': self._last_cleanup_time.isoformat() if self._last_cleanup_time else None,
            'total_files_deleted': self._total_files_deleted,
            'total_bytes_freed': self._total_bytes_freed,
            'scheduler_running': self._cleanup_thread is not None and self._cleanup_thread.is_alive()
        }
        return stats
