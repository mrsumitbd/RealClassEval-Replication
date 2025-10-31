
import os
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional


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
        self._cleanup_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._last_cleanup_time: Optional[datetime] = None
        self._cleanup_stats: Dict[str, int] = {
            'total_files': 0,
            'deleted_files': 0,
            'last_cleanup_time': None
        }

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        if self._cleanup_thread is not None and self._cleanup_thread.is_alive():
            return

        self._stop_event.clear()
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_loop,
            daemon=True
        )
        self._cleanup_thread.start()

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        if self._cleanup_thread is not None:
            self._stop_event.set()
            self._cleanup_thread.join(timeout=5)
            self._cleanup_thread = None

    def _cleanup_loop(self):
        '''Background loop for periodic cleanup'''
        while not self._stop_event.is_set():
            current_time = datetime.now()
            if (self._last_cleanup_time is None or
                    (current_time - self._last_cleanup_time) >= timedelta(hours=self.cleanup_interval_hours)):
                self.cleanup_old_logs()
                self._last_cleanup_time = current_time

            # Sleep for a while before checking again
            time.sleep(3600)  # Check every hour

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        if not os.path.exists(self.log_dir):
            return

        now = datetime.now()
        cutoff_time = now - timedelta(days=self.max_age_days)
        deleted_files = 0
        total_files = 0

        for filename in os.listdir(self.log_dir):
            filepath = os.path.join(self.log_dir, filename)
            if os.path.isfile(filepath):
                total_files += 1
                file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if file_mtime < cutoff_time:
                    try:
                        os.remove(filepath)
                        deleted_files += 1
                    except OSError as e:
                        print(f"Error deleting file {filepath}: {e}")

        self._cleanup_stats.update({
            'total_files': total_files,
            'deleted_files': deleted_files,
            'last_cleanup_time': now.timestamp()
        })

    def get_cleanup_stats(self) -> dict:
        '''Get statistics about log files and cleanup status'''
        return self._cleanup_stats.copy()
