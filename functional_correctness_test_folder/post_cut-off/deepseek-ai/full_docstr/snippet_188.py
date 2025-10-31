
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
        self._scheduler_thread = None
        self._stop_event = threading.Event()
        self._stats = {
            'total_logs': 0,
            'deleted_logs': 0,
            'last_cleanup_time': None,
            'next_cleanup_time': None
        }

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        if self._scheduler_thread is not None and self._scheduler_thread.is_alive():
            return
        self._stop_event.clear()
        self._scheduler_thread = threading.Thread(
            target=self._cleanup_loop, daemon=True)
        self._scheduler_thread.start()

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        self._stop_event.set()
        if self._scheduler_thread is not None:
            self._scheduler_thread.join()
            self._scheduler_thread = None

    def _cleanup_loop(self):
        '''Background loop for periodic cleanup'''
        while not self._stop_event.is_set():
            self.cleanup_old_logs()
            self._stats['next_cleanup_time'] = datetime.now(
            ) + timedelta(hours=self.cleanup_interval_hours)
            self._stop_event.wait(self.cleanup_interval_hours * 3600)

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        now = datetime.now()
        cutoff_time = now - timedelta(days=self.max_age_days)
        deleted_count = 0
        total_count = 0

        for filename in os.listdir(self.log_dir):
            filepath = os.path.join(self.log_dir, filename)
            if os.path.isfile(filepath):
                total_count += 1
                file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if file_mtime < cutoff_time:
                    try:
                        os.remove(filepath)
                        deleted_count += 1
                    except OSError:
                        pass

        self._stats['total_logs'] = total_count
        self._stats['deleted_logs'] = deleted_count
        self._stats['last_cleanup_time'] = now

    def get_cleanup_stats(self) -> Dict:
        '''Get statistics about log files and cleanup status'''
        return self._stats.copy()
