import os
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional


class LogCleanupManager:

    def __init__(self, log_dir: str, max_age_days: int = 30, cleanup_interval_hours: int = 24):
        '''
        Initialize log cleanup manager.
        Args:
            log_dir: Directory containing log files
            max_age_days: Maximum age of log files in days (default: 30 days)
            cleanup_interval_hours: Cleanup interval in hours (default: 24 hours)
        '''
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.max_age_days = max(0, int(max_age_days))
        self.cleanup_interval_hours = max(1, int(cleanup_interval_hours))

        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

        self._stats: Dict[str, Optional[object]] = {
            "scheduler_running": False,
            "last_cleanup_time": None,
            "last_run_duration_seconds": None,
            "files_scanned": 0,
            "files_deleted": 0,
            "bytes_freed": 0,
            "errors": 0,
            "last_error": None,
            "log_dir": str(self.log_dir),
            "max_age_days": self.max_age_days,
            "cleanup_interval_hours": self.cleanup_interval_hours,
        }

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        with self._lock:
            if self._thread and self._thread.is_alive():
                return
            self._stop_event.clear()
            self._thread = threading.Thread(
                target=self._cleanup_loop, name="LogCleanupScheduler", daemon=True)
            self._stats["scheduler_running"] = True
            self._thread.start()

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        self._stop_event.set()
        thread = None
        with self._lock:
            thread = self._thread
        if thread and thread.is_alive():
            thread.join(timeout=5.0)
        with self._lock:
            self._stats["scheduler_running"] = False
            self._thread = None

    def _cleanup_loop(self):
        interval_seconds = self.cleanup_interval_hours * 3600
        while not self._stop_event.is_set():
            self.cleanup_old_logs()
            if self._stop_event.wait(interval_seconds):
                break

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        start = time.time()
        files_scanned = 0
        files_deleted = 0
        bytes_freed = 0
        errors = 0
        last_error = None

        try:
            now = time.time()
            max_age_seconds = self.max_age_days * 86400
            # age 0 -> only delete files older than now (effectively none)
            cutoff = now - max_age_seconds if self.max_age_days > 0 else now

            if not self.log_dir.exists():
                self.log_dir.mkdir(parents=True, exist_ok=True)

            for entry in self.log_dir.iterdir():
                try:
                    if not entry.is_file():
                        continue
                    files_scanned += 1

                    try:
                        stat = entry.stat()
                    except OSError as e:
                        errors += 1
                        last_error = repr(e)
                        continue

                    mtime = stat.st_mtime
                    if mtime <= cutoff:
                        size = stat.st_size
                        try:
                            entry.unlink(missing_ok=True)
                            files_deleted += 1
                            bytes_freed += size
                        except OSError as e:
                            errors += 1
                            last_error = repr(e)
                except Exception as e:
                    errors += 1
                    last_error = repr(e)
        finally:
            duration = time.time() - start
            with self._lock:
                self._stats["last_cleanup_time"] = datetime.utcnow(
                ).isoformat() + "Z"
                self._stats["last_run_duration_seconds"] = round(duration, 6)
                # Aggregate totals
                self._stats["files_scanned"] = (
                    self._stats.get("files_scanned") or 0) + files_scanned
                self._stats["files_deleted"] = (
                    self._stats.get("files_deleted") or 0) + files_deleted
                self._stats["bytes_freed"] = (
                    self._stats.get("bytes_freed") or 0) + bytes_freed
                self._stats["errors"] = (
                    self._stats.get("errors") or 0) + errors
                if last_error:
                    self._stats["last_error"] = last_error

    def get_cleanup_stats(self) -> dict:
        '''Get statistics about log files and cleanup status'''
        with self._lock:
            stats_copy = dict(self._stats)
        # Add current directory snapshot info
        try:
            total_files = 0
            total_size = 0
            oldest_file_mtime = None
            newest_file_mtime = None
            if self.log_dir.exists():
                for entry in self.log_dir.iterdir():
                    if not entry.is_file():
                        continue
                    total_files += 1
                    try:
                        st = entry.stat()
                        total_size += st.st_size
                        if oldest_file_mtime is None or st.st_mtime < oldest_file_mtime:
                            oldest_file_mtime = st.st_mtime
                        if newest_file_mtime is None or st.st_mtime > newest_file_mtime:
                            newest_file_mtime = st.st_mtime
                    except OSError:
                        continue
            stats_copy["current_files"] = total_files
            stats_copy["current_total_size"] = total_size
            stats_copy["current_oldest_mtime"] = (
                datetime.utcfromtimestamp(oldest_file_mtime).isoformat() + "Z"
                if oldest_file_mtime is not None else None
            )
            stats_copy["current_newest_mtime"] = (
                datetime.utcfromtimestamp(newest_file_mtime).isoformat() + "Z"
                if newest_file_mtime is not None else None
            )
        except Exception as e:
            stats_copy["last_error"] = repr(e)
        return stats_copy
