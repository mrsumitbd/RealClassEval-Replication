
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
        self.cleanup_thread = None
        self.stop_event = threading.Event()
        self.cleanup_stats = {'files_deleted': 0, 'files_checked': 0}

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        if self.cleanup_thread is None:
            self.cleanup_thread = threading.Thread(target=self._cleanup_loop)
            self.cleanup_thread.start()

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        if self.cleanup_thread is not None:
            self.stop_event.set()
            self.cleanup_thread.join()
            self.cleanup_thread = None

    def _cleanup_loop(self):
        '''Background loop for periodic cleanup'''
        while not self.stop_event.is_set():
            self.cleanup_old_logs()
            time.sleep(self.cleanup_interval_hours * 3600)

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        now = datetime.now()
        max_age = timedelta(days=self.max_age_days)
        for filename in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, filename)
            if os.path.isfile(file_path):
                file_stat = os.stat(file_path)
                file_age = now - datetime.fromtimestamp(file_stat.st_mtime)
                self.cleanup_stats['files_checked'] += 1
                if file_age > max_age:
                    os.remove(file_path)
                    self.cleanup_stats['files_deleted'] += 1

    def get_cleanup_stats(self) -> dict:
        '''Get statistics about log files and cleanup status'''
        return self.cleanup_stats.copy()
