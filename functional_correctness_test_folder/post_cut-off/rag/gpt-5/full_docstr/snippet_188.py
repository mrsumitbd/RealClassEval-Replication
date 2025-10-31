import os
import threading
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional


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
        if max_age_days < 0:
            raise ValueError('max_age_days must be >= 0')
        if cleanup_interval_hours <= 0:
            raise ValueError('cleanup_interval_hours must be > 0')

        self.log_dir = Path(log_dir).expanduser()
        self.max_age_days = int(max_age_days)
        self.cleanup_interval_hours = float(cleanup_interval_hours)
        self._interval_seconds = int(self.cleanup_interval_hours * 3600)

        self._logger = logging.getLogger(f'{__name__}.LogCleanupManager')
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

        self._created_at = time.time()
        self._scheduler_started_at: Optional[float] = None

        # Stats
        self._stats = {
            'created_at': self._created_at,
            'scheduler_started_at': None,
            'last_run': None,
            'last_duration_s': None,
            'total_runs': 0,
            'files_scanned_last': 0,
            'files_deleted_last': 0,
            'bytes_freed_last': 0,
            'errors_last': 0,
            'files_scanned_total': 0,
            'files_deleted_total': 0,
            'bytes_freed_total': 0,
            'last_error': None,
        }

        os.makedirs(self.log_dir, exist_ok=True)

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._cleanup_loop, name='LogCleanupScheduler', daemon=True)
        self._scheduler_started_at = time.time()
        self._stats['scheduler_started_at'] = self._scheduler_started_at
        self._thread.start()

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        if not self._thread:
            return
        self._stop_event.set()
        self._thread.join(timeout=self._interval_seconds + 5)
        self._thread = None

    def _cleanup_loop(self):
        '''Background loop for periodic cleanup'''
        # Run immediately once, then at intervals
        while not self._stop_event.is_set():
            start_ts = time.time()
            try:
                self.cleanup_old_logs()
            except Exception as e:
                # Any unexpected exception shouldn't crash the loop
                self._logger.exception(
                    'Unexpected error during cleanup loop: %s', e)
            # Wait for the next interval
            elapsed = max(0.0, time.time() - start_ts)
            # ensure at least some wait
            wait_for = max(1.0, self._interval_seconds)
            # Use event wait to allow responsive shutdown
            if self._stop_event.wait(wait_for):
                break

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        if not self.log_dir.exists():
            return

        if not self._lock.acquire(blocking=False):
            # Skip overlapping runs
            return
        try:
            run_start = time.time()
            threshold_ts = run_start - (self.max_age_days * 86400)

            files_scanned = 0
            files_deleted = 0
            bytes_freed = 0
            errors = 0
            last_error_msg = None

            try:
                entries = list(self.log_dir.iterdir())
            except Exception as e:
                # If we cannot list the directory, record and abort this run
                last_error_msg = f'Failed to list directory: {e}'
                errors += 1
                entries = []

            for entry in entries:
                try:
                    # Only regular files; skip dirs and symlinks for safety
                    if not entry.is_file() or entry.is_symlink():
                        continue
                    files_scanned += 1
                    try:
                        st = entry.stat()
                    except FileNotFoundError:
                        # File removed between iterdir and stat
                        continue
                    except Exception as e:
                        errors += 1
                        last_error_msg = f'stat failed for {entry}: {e}'
                        continue

                    if st.st_mtime < threshold_ts:
                        size = st.st_size
                        try:
                            entry.unlink()
                            files_deleted += 1
                            bytes_freed += size
                        except FileNotFoundError:
                            # Already gone
                            continue
                        except Exception as e:
                            errors += 1
                            last_error_msg = f'failed to delete {entry}: {e}'
                except Exception as e:
                    errors += 1
                    last_error_msg = f'iteration error for {entry}: {e}'

            duration = time.time() - run_start

            # Update stats
            self._stats['last_run'] = run_start
            self._stats['last_duration_s'] = duration
            self._stats['total_runs'] += 1
            self._stats['files_scanned_last'] = files_scanned
            self._stats['files_deleted_last'] = files_deleted
            self._stats['bytes_freed_last'] = bytes_freed
            self._stats['errors_last'] = errors
            self._stats['files_scanned_total'] += files_scanned
            self._stats['files_deleted_total'] += files_deleted
            self._stats['bytes_freed_total'] += bytes_freed
            self._stats['last_error'] = last_error_msg

        finally:
            self._lock.release()

    def get_cleanup_stats(self) -> dict:
        '''Get statistics about log files and cleanup status'''
        with self._lock:
            stats_copy: Dict[str, Any] = dict(self._stats)
        # Provide a stable, JSON-friendly summary
        return {
            'log_dir': str(self.log_dir),
            'max_age_days': self.max_age_days,
            'cleanup_interval_hours': self.cleanup_interval_hours,
            'scheduler_running': bool(self._thread and self._thread.is_alive()),
            'created_at': stats_copy.get('created_at'),
            'scheduler_started_at': stats_copy.get('scheduler_started_at'),
            'last_run': stats_copy.get('last_run'),
            'last_duration_s': stats_copy.get('last_duration_s'),
            'total_runs': stats_copy.get('total_runs'),
            'files_scanned_last': stats_copy.get('files_scanned_last'),
            'files_deleted_last': stats_copy.get('files_deleted_last'),
            'bytes_freed_last': stats_copy.get('bytes_freed_last'),
            'errors_last': stats_copy.get('errors_last'),
            'files_scanned_total': stats_copy.get('files_scanned_total'),
            'files_deleted_total': stats_copy.get('files_deleted_total'),
            'bytes_freed_total': stats_copy.get('bytes_freed_total'),
            'last_error': stats_copy.get('last_error'),
        }
