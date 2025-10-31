
import os
import time
import threading
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any


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
        self.log_dir = Path(log_dir).expanduser().resolve()
        if not self.log_dir.is_dir():
            raise ValueError(f'log_dir {self.log_dir} is not a directory')
        self.max_age = timedelta(days=max_age_days)
        self.interval = timedelta(hours=cleanup_interval_hours)
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()
        self._stats: Dict[str, Any] = {
            'total_files': 0,
            'deleted_files': 0,
            'last_cleanup': None,
            'last_cleanup_success': None,
            'last_error': None,
        }

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        if self._thread and self._thread.is_alive():
            logging.debug('Cleanup scheduler already running')
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._cleanup_loop, name='LogCleanupThread', daemon=True)
        self._thread.start()
        logging.info('Started log cleanup scheduler')

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        if not self._thread:
            return
        self._stop_event.set()
        self._thread.join()
        self._thread = None
        logging.info('Stopped log cleanup scheduler')

    def _cleanup_loop(self):
        '''Background loop for periodic cleanup'''
        while not self._stop_event.is_set():
            try:
                self.cleanup_old_logs()
            except Exception as exc:
                logging.exception('Error during log cleanup: %s', exc)
                with self._lock:
                    self._stats['last_error'] = str(exc)
            # Wait for the next interval or until stop event
            if self._stop_event.wait(self.interval.total_seconds()):
                break

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        now = datetime.now()
        deleted = 0
        total = 0
        for entry in self.log_dir.iterdir():
            if not entry.is_file():
                continue
            total += 1
            try:
                mtime = datetime.fromtimestamp(entry.stat().st_mtime)
            except OSError:
                continue
            if now - mtime > self.max_age:
                try:
                    entry.unlink()
                    deleted += 1
                    logging.debug('Deleted old log file: %s', entry)
                except OSError as exc:
                    logging.warning('Failed to delete %s: %s', entry, exc)
        with self._lock:
            self._stats.update({
                'total_files': total,
                'deleted_files': deleted,
                'last_cleanup': now.isoformat(),
                'last_cleanup_success': True,
                'last_error': None,
            })
        logging.info(
            'Cleanup complete: %d files deleted out of %d', deleted, total)

    def get_cleanup_stats(self) -> dict:
        '''Get statistics about log files and cleanup status'''
        with self._lock:
            return dict(self._stats)
