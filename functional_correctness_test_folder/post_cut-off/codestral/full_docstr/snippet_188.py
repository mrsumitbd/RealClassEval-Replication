
import os
import time
import threading
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
        self.cleanup_stats = {
            'last_cleanup_time': None,
            'total_files': 0,
            'deleted_files': 0,
            'remaining_files': 0
        }
        self._stop_event = threading.Event()
        self._cleanup_thread = None

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        if self._cleanup_thread is None or not self._cleanup_thread.is_alive():
            self._stop_event.clear()
            self._cleanup_thread = threading.Thread(target=self._cleanup_loop)
            self._cleanup_thread.daemon = True
            self._cleanup_thread.start()

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        if self._cleanup_thread is not None and self._cleanup_thread.is_alive():
            self._stop_event.set()
            self._cleanup_thread.join()

    def _cleanup_loop(self):
        '''Background loop for periodic cleanup'''
        while not self._stop_event.is_set():
            self.cleanup_old_logs()
            self._stop_event.wait(self.cleanup_interval_hours * 3600)

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        now = datetime.now()
        max_age = timedelta(days=self.max_age_days)
        deleted_files = 0
        total_files = 0

        for filename in os.listdir(self.log_dir):
            filepath = os.path.join(self.log_dir, filename)
            if os.path.isfile(filepath):
                total_files += 1
                file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if now - file_mtime > max_age:
                    os.remove(filepath)
                    deleted_files += 1

        self.cleanup_stats.update({
            'last_cleanup_time': now,
            'total_files': total_files,
            'deleted_files': deleted_files,
            'remaining_files': total_files - deleted_files
        })

    def get_cleanup_stats(self) -> dict:
        '''Get statistics about log files and cleanup status'''
        return self.cleanup_stats
