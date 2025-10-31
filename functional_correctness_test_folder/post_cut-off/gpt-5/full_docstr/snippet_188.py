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
        import os
        from datetime import timedelta

        if not isinstance(log_dir, str) or not log_dir:
            raise ValueError("log_dir must be a non-empty string")
        if not isinstance(max_age_days, int) or max_age_days < 0:
            raise ValueError("max_age_days must be a non-negative integer")
        if not isinstance(cleanup_interval_hours, int) or cleanup_interval_hours <= 0:
            raise ValueError(
                "cleanup_interval_hours must be a positive integer")

        self.log_dir = os.path.abspath(log_dir)
        self.max_age_days = max_age_days
        self.cleanup_interval_hours = cleanup_interval_hours
        self._max_age_delta = timedelta(days=max_age_days)

        import threading
        self._stop_event = threading.Event()
        self._thread = None
        self._lock = threading.Lock()

        self._stats = {
            "scheduler_running": False,
            "last_cleanup_time": None,
            "last_run_duration_seconds": None,
            "files_deleted_last_run": 0,
            "bytes_freed_last_run": 0,
            "files_scanned_last_run": 0,
            "total_cleanups": 0,
            "total_files_deleted": 0,
            "total_bytes_freed": 0,
            "total_files_scanned": 0,
            "last_error": None,
        }

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        import threading

        with self._lock:
            if self._thread and self._thread.is_alive():
                return False
            self._stop_event.clear()
            self._thread = threading.Thread(
                target=self._cleanup_loop, name="LogCleanupManagerThread", daemon=True)
            self._thread.start()
            self._stats["scheduler_running"] = True
            return True

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        with self._lock:
            thread = self._thread
        if not thread:
            with self._lock:
                self._stats["scheduler_running"] = False
            return False
        self._stop_event.set()
        thread.join(timeout=self.cleanup_interval_hours * 3600 + 5)
        with self._lock:
            running = thread.is_alive()
            self._stats["scheduler_running"] = not running
            if not running:
                self._thread = None
        return True

    def _cleanup_loop(self):
        import time
        interval_seconds = max(1, int(self.cleanup_interval_hours * 3600))
        while not self._stop_event.is_set():
            self.cleanup_old_logs()
            if self._stop_event.wait(interval_seconds):
                break

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        import os
        import time
        from datetime import datetime, timezone

        start = time.perf_counter()
        files_deleted = 0
        bytes_freed = 0
        files_scanned = 0
        last_error = None

        now = datetime.now(timezone.utc)
        cutoff_ts = (now - self._max_age_delta).timestamp()

        try:
            if not os.path.isdir(self.log_dir):
                raise FileNotFoundError(
                    f"Log directory not found: {self.log_dir}")

            with os.scandir(self.log_dir) as it:
                for entry in it:
                    try:
                        if not entry.is_file(follow_symlinks=False):
                            continue
                        files_scanned += 1
                        try:
                            stat = entry.stat(follow_symlinks=False)
                        except FileNotFoundError:
                            continue
                        mtime = stat.st_mtime
                        if mtime <= cutoff_ts:
                            size = stat.st_size
                            try:
                                os.remove(entry.path)
                                files_deleted += 1
                                bytes_freed += size
                            except FileNotFoundError:
                                continue
                            except PermissionError as e:
                                last_error = str(e)
                            except OSError as e:
                                last_error = str(e)
                    except Exception as e:
                        last_error = str(e)
                        continue
        except Exception as e:
            last_error = str(e)

        duration = time.perf_counter() - start
        with self._lock:
            self._stats["last_cleanup_time"] = datetime.now(
                timezone.utc).isoformat()
            self._stats["last_run_duration_seconds"] = duration
            self._stats["files_deleted_last_run"] = files_deleted
            self._stats["bytes_freed_last_run"] = bytes_freed
            self._stats["files_scanned_last_run"] = files_scanned
            self._stats["total_cleanups"] += 1
            self._stats["total_files_deleted"] += files_deleted
            self._stats["total_bytes_freed"] += bytes_freed
            self._stats["total_files_scanned"] += files_scanned
            self._stats["last_error"] = last_error

        return {
            "files_deleted": files_deleted,
            "bytes_freed": bytes_freed,
            "files_scanned": files_scanned,
            "duration_seconds": duration,
            "error": last_error,
        }

    def get_cleanup_stats(self) -> dict:
        '''Get statistics about log files and cleanup status'''
        with self._lock:
            return dict(self._stats)
