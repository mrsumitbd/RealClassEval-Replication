
import os
import time
import threading
from datetime import datetime, timedelta
from typing import Dict


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
        while not self._stop_event.is_set():
            self.cleanup_old_logs()
            time.sleep(self.cleanup_interval_hours * 3600)

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        if not os.path.exists(self.log_dir):
            return

        current_time = datetime.now()
        max_age = timedelta(days=self.max_age_days)
        deleted_logs = 0
        total_logs = 0

        for filename in os.listdir(self.log_dir):
            filepath = os.path.join(self.log_dir, filename)
            if os.path.isfile(filepath):
                total_logs += 1
                file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if current_time - file_mtime > max_age:
                    try:
                        os.remove(filepath)
                        deleted_logs += 1
                    except OSError:
                        pass

        self._stats['total_logs'] = total_logs
        self._stats['deleted_logs'] = deleted_logs
        self._stats['last_cleanup_time'] = datetime.now()
        self._stats['next_cleanup_time'] = datetime.now(
        ) + timedelta(hours=self.cleanup_interval_hours)

    def get_cleanup_stats(self) -> Dict:
        '''Get statistics about log files and cleanup status'''
        return self._stats.copy()
