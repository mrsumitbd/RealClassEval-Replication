
import os
import time
import datetime
import threading
import logging
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
        self.max_age_days = max_age_days
        self.cleanup_interval = cleanup_interval_hours * 3600  # seconds
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()
        self._stats: Dict[str, Any] = {
            'last_cleanup': None,
            'files_scanned': 0,
            'files_deleted': 0,
            'errors': 0,
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
        logging.info('Log cleanup scheduler started')

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        if not self._thread:
            return
        self._stop_event.set()
        self._thread.join()
        self._thread = None
        logging.info('Log cleanup scheduler stopped')

    def _cleanup_loop(self):
        '''Background loop for periodic cleanup'''
        while not self._stop_event.is_set():
            start = time.time()
            try:
                self.cleanup_old_logs()
            except Exception as exc:
                logging.exception(
                    'Unexpected error during log cleanup: %s', exc)
            elapsed = time.time() - start
            # Sleep until next interval or until stop event
            wait = max(0, self.cleanup_interval - elapsed)
            if self._stop_event.wait(wait):
                break

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        now = datetime.datetime.now()
        cutoff = now - datetime.timedelta(days=self.max_age_days)
        scanned = 0
        deleted = 0
        errors = 0

        for entry in self.log_dir.iterdir():
            if not entry.is_file():
                continue
            try:
                mtime = datetime.datetime.fromtimestamp(entry.stat().st_mtime)
                scanned += 1
                if mtime < cutoff:
                    try:
                        entry.unlink()
                        deleted += 1
                        logging.debug('Deleted old log file: %s', entry)
                    except Exception as e:
                        errors += 1
                        logging.warning('Failed to delete %s: %s', entry, e)
            except Exception as e:
                errors += 1
                logging.warning('Failed to process %s: %s', entry, e)

        with self._lock:
            self._stats.update({
                'last_cleanup': now.isoformat(),
                'files_scanned': scanned,
                'files_deleted': deleted,
                'errors': errors,
            })
        logging.info('Log cleanup finished: scanned=%d deleted=%d errors=%d',
                     scanned, deleted, errors)

    def get_cleanup_stats(self) -> dict:
        '''Get statistics about log files and cleanup status'''
        with self._lock:
            return dict(self._stats)
