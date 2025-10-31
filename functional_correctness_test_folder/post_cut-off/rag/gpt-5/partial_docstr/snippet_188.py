import os
import time
import threading
from typing import Optional, Dict
from datetime import datetime, timezone


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
        if not isinstance(log_dir, str) or not log_dir:
            raise ValueError('log_dir must be a non-empty string')
        if max_age_days < 0:
            raise ValueError('max_age_days must be >= 0')
        if cleanup_interval_hours <= 0:
            raise ValueError('cleanup_interval_hours must be > 0')

        self.log_dir = os.path.abspath(log_dir)
        os.makedirs(self.log_dir, exist_ok=True)

        self.max_age_days = int(max_age_days)
        self.cleanup_interval_hours = float(cleanup_interval_hours)

        self._interval_seconds = int(self.cleanup_interval_hours * 3600)
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

        now_iso = None
        self._stats: Dict[str, object] = {
            'log_dir': self.log_dir,
            'max_age_days': self.max_age_days,
            'cleanup_interval_hours': self.cleanup_interval_hours,
            'runs': 0,
            'files_scanned': 0,
            'files_deleted': 0,
            'bytes_scanned': 0,
            'bytes_freed': 0,
            'last_run': now_iso,
            'last_success': now_iso,
            'last_duration_seconds': 0.0,
            'last_error': None,
            'last_run_stats': {
                'files_scanned': 0,
                'files_deleted': 0,
                'bytes_scanned': 0,
                'bytes_freed': 0,
                'errors': 0,
            },
            'scheduler_running': False,
            'scheduler_started_at': None,
        }

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        with self._lock:
            if self._thread and self._thread.is_alive():
                self._stats['scheduler_running'] = True
                return
            self._stop_event.clear()
            self._thread = threading.Thread(
                target=self._cleanup_loop, name='LogCleanupManager', daemon=True)
            self._thread.start()
            self._stats['scheduler_running'] = True
            self._stats['scheduler_started_at'] = datetime.now(
                timezone.utc).isoformat()

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        self._stop_event.set()
        t = self._thread
        if t and t.is_alive():
            t.join(timeout=self._interval_seconds + 5)
        with self._lock:
            self._stats['scheduler_running'] = False
        self._thread = None

    def _cleanup_loop(self):
        # Run immediately once, then wait for interval between subsequent runs
        if not self._stop_event.is_set():
            try:
                self.cleanup_old_logs()
            except Exception:
                pass
        while not self._stop_event.is_set():
            if self._stop_event.wait(self._interval_seconds):
                break
            try:
                self.cleanup_old_logs()
            except Exception:
                # Swallow to keep the loop alive
                pass

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        start_time = time.time()
        cutoff_ts = start_time - (self.max_age_days * 86400)

        run_files_scanned = 0
        run_files_deleted = 0
        run_bytes_scanned = 0
        run_bytes_freed = 0
        run_errors = 0
        last_error_msg = None

        try:
            with os.scandir(self.log_dir) as it:
                for entry in it:
                    try:
                        # Only consider regular files (not directories). Do not follow symlinks when checking metadata.
                        if not entry.is_file(follow_symlinks=False):
                            continue
                        st = entry.stat(follow_symlinks=False)
                        size = int(st.st_size)
                        mtime = float(st.st_mtime)

                        run_files_scanned += 1
                        run_bytes_scanned += size

                        if mtime < cutoff_ts:
                            try:
                                os.remove(entry.path)
                                run_files_deleted += 1
                                run_bytes_freed += size
                            except OSError as e:
                                run_errors += 1
                                last_error_msg = f'Failed to delete {entry.path}: {e}'
                    except OSError as e:
                        run_errors += 1
                        last_error_msg = f'Failed to stat {entry.path if hasattr(entry, "path") else "entry"}: {e}'
        except FileNotFoundError:
            # Directory removed outside; treat as no files to clean
            pass
        except Exception as e:
            run_errors += 1
            last_error_msg = f'Unexpected error during cleanup: {e}'

        duration = time.time() - start_time
        now_iso = datetime.now(timezone.utc).isoformat()

        with self._lock:
            self._stats['runs'] = int(self._stats.get('runs', 0)) + 1
            self._stats['files_scanned'] = int(
                self._stats.get('files_scanned', 0)) + run_files_scanned
            self._stats['files_deleted'] = int(
                self._stats.get('files_deleted', 0)) + run_files_deleted
            self._stats['bytes_scanned'] = int(
                self._stats.get('bytes_scanned', 0)) + run_bytes_scanned
            self._stats['bytes_freed'] = int(
                self._stats.get('bytes_freed', 0)) + run_bytes_freed
            self._stats['last_run'] = now_iso
            if run_errors == 0:
                self._stats['last_success'] = now_iso
                self._stats['last_error'] = None
            else:
                self._stats['last_error'] = last_error_msg
            self._stats['last_duration_seconds'] = float(duration)
            self._stats['last_run_stats'] = {
                'files_scanned': run_files_scanned,
                'files_deleted': run_files_deleted,
                'bytes_scanned': run_bytes_scanned,
                'bytes_freed': run_bytes_freed,
                'errors': run_errors,
            }

    def get_cleanup_stats(self) -> dict:
        '''Get statistics about log files and cleanup status'''
        with self._lock:
            stats_copy = dict(self._stats)
            stats_copy['last_run_stats'] = dict(
                self._stats.get('last_run_stats', {}))
            # Add dynamic fields
            if stats_copy.get('scheduler_running') and self._stats.get('last_run'):
                try:
                    last_run_dt = datetime.fromisoformat(
                        self._stats['last_run'])
                    elapsed = (datetime.now(timezone.utc) -
                               last_run_dt).total_seconds()
                    next_in = max(0, self._interval_seconds - int(elapsed))
                except Exception:
                    next_in = self._interval_seconds
            else:
                next_in = None
            stats_copy['next_run_in_seconds'] = next_in
            return stats_copy
