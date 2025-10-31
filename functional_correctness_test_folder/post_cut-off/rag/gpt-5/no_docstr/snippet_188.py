import os
import time
import threading
from datetime import datetime, timedelta
from typing import Dict
import stat


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
        self.log_dir = os.path.abspath(log_dir)
        if os.path.exists(self.log_dir):
            if not os.path.isdir(self.log_dir):
                raise ValueError(
                    f'log_dir must be a directory: {self.log_dir}')
        else:
            os.makedirs(self.log_dir, exist_ok=True)

        self.max_age_days = max(0.0, float(max_age_days))
        self.cleanup_interval_sec = max(
            1.0, float(cleanup_interval_hours) * 3600.0)

        self._stop_event = threading.Event()
        self._thread = None
        self._lock = threading.Lock()
        self._cleanup_lock = threading.Lock()

        self._stats: Dict[str, object] = {
            'files_examined': 0,
            'files_deleted': 0,
            'bytes_freed': 0,
            'last_cleanup_start': None,
            'last_cleanup_end': None,
            'last_run_duration_sec': None,
            'last_error': None,
            'runs': 0,
            'errors': 0,
            'scheduler_running': False,
            'next_scheduled_time': None,
        }

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        with self._lock:
            if self._thread and self._thread.is_alive():
                return
            self._stop_event.clear()
            self._stats['scheduler_running'] = True
            self._thread = threading.Thread(
                target=self._cleanup_loop, name='LogCleanupManager', daemon=True)
            self._thread.start()

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        with self._lock:
            if not self._thread:
                self._stats['scheduler_running'] = False
                return
            self._stop_event.set()
            thread = self._thread
        thread.join()
        with self._lock:
            self._stats['scheduler_running'] = False
            self._thread = None
            self._stats['next_scheduled_time'] = None

    def _cleanup_loop(self):
        while not self._stop_event.is_set():
            start = time.time()
            try:
                self.cleanup_old_logs()
            except Exception as e:
                with self._lock:
                    self._stats['errors'] = int(
                        self._stats.get('errors') or 0) + 1
                    self._stats['last_error'] = repr(e)
            next_time = start + self.cleanup_interval_sec
            with self._lock:
                self._stats['next_scheduled_time'] = datetime.fromtimestamp(
                    next_time).isoformat()
            remaining = max(0.0, next_time - time.time())
            if self._stop_event.wait(remaining):
                break

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        with self._cleanup_lock:
            start_time = time.time()
            cutoff = start_time - (self.max_age_days * 86400.0)

            files_examined = 0
            files_deleted = 0
            bytes_freed = 0
            last_error = None

            for root, _, files in os.walk(self.log_dir):
                for name in files:
                    path = os.path.join(root, name)
                    try:
                        st = os.lstat(path)
                    except FileNotFoundError:
                        continue
                    except Exception as e:
                        last_error = repr(e)
                        continue
                    mode = st.st_mode
                    if not (stat.S_ISREG(mode) or stat.S_ISLNK(mode)):
                        continue
                    files_examined += 1
                    try:
                        mtime = st.st_mtime
                    except Exception:
                        # If mtime is not accessible, skip
                        continue
                    if mtime < cutoff:
                        try:
                            size = st.st_size
                            os.remove(path)
                            files_deleted += 1
                            bytes_freed += int(size)
                        except FileNotFoundError:
                            continue
                        except Exception as e:
                            last_error = repr(e)
                            continue

            end_time = time.time()
            with self._lock:
                self._stats['files_examined'] = int(
                    self._stats.get('files_examined') or 0) + files_examined
                self._stats['files_deleted'] = int(
                    self._stats.get('files_deleted') or 0) + files_deleted
                self._stats['bytes_freed'] = int(
                    self._stats.get('bytes_freed') or 0) + bytes_freed
                self._stats['last_cleanup_start'] = datetime.fromtimestamp(
                    start_time).isoformat()
                self._stats['last_cleanup_end'] = datetime.fromtimestamp(
                    end_time).isoformat()
                self._stats['last_run_duration_sec'] = end_time - start_time
                self._stats['runs'] = int(self._stats.get('runs') or 0) + 1
                if last_error is not None:
                    self._stats['errors'] = int(
                        self._stats.get('errors') or 0) + 1
                    self._stats['last_error'] = last_error

    def get_cleanup_stats(self) -> dict:
        '''Get statistics about log files and cleanup status'''
        total_files = 0
        total_bytes = 0
        try:
            for root, _, files in os.walk(self.log_dir):
                for name in files:
                    path = os.path.join(root, name)
                    try:
                        st = os.lstat(path)
                    except Exception:
                        continue
                    if stat.S_ISREG(st.st_mode) or stat.S_ISLNK(st.st_mode):
                        total_files += 1
                        total_bytes += int(getattr(st, 'st_size', 0))
        except Exception:
            pass

        with self._lock:
            stats_copy = dict(self._stats)
        stats_copy['current_total_files'] = total_files
        stats_copy['current_total_bytes'] = total_bytes
        stats_copy['log_dir'] = self.log_dir
        stats_copy['max_age_days'] = self.max_age_days
        stats_copy['cleanup_interval_hours'] = self.cleanup_interval_sec / 3600.0
        return stats_copy
