
import os
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional


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
        self.log_dir = Path(log_dir)
        if not self.log_dir.is_dir():
            raise ValueError(f"'{log_dir}' is not a valid directory")

        self.max_age = timedelta(days=max_age_days)
        self.interval = timedelta(hours=cleanup_interval_hours)

        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

        # Statistics
        self._stats: Dict[str, any] = {
            'total_files': 0,
            'deleted_files': 0,
            'last_cleanup': None,
            'next_cleanup': None,
            'errors': 0,
        }

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        with self._lock:
            if self._thread and self._thread.is_alive():
                return  # already running
            self._stop_event.clear()
            self._thread = threading.Thread(
                target=self._cleanup_loop, daemon=True)
            self._thread.start()

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        self._stop_event.set()
        if self._thread:
            self._thread.join()
            self._thread = None

    def _cleanup_loop(self):
        '''Background loop for periodic cleanup'''
        while not self._stop_event.is_set():
            now = datetime.now()
            with self._lock:
                self._stats['next_cleanup'] = now + self.interval
            self.cleanup_old_logs()
            # Wait for the next interval or until stopped
            if self._stop_event.wait(self.interval.total_seconds()):
                break

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        deleted = 0
        errors = 0
        total = 0
        cutoff = datetime.now() - self.max_age

        for entry in self.log_dir.iterdir():
            if not entry.is_file():
                continue
            total += 1
            try:
                mtime = datetime.fromtimestamp(entry.stat().st_mtime)
                if mtime < cutoff:
                    entry.unlink()
                    deleted += 1
            except Exception:
                errors += 1

        with self._lock:
            self._stats.update({
                'total_files': total,
                'deleted_files': deleted,
                'last_cleanup': datetime.now(),
                'errors': errors,
            })

    def get_cleanup_stats(self) -> Dict[str, any]:
        '''Get statistics about log files and cleanup status'''
        with self._lock:
            return dict(self._stats)
