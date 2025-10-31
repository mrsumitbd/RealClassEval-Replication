
import os
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any


class LogCleanupManager:
    def __init__(self, log_dir: str, max_age_days: int = 30, cleanup_interval_hours: int = 24):
        self.log_dir = Path(log_dir)
        self.max_age_days = max_age_days
        self.cleanup_interval_hours = cleanup_interval_hours

        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

        # Stats
        self._last_cleanup_time: datetime | None = None
        self._files_deleted: int = 0
        self._bytes_freed: int = 0
        self._lock = threading.Lock()

    def start_cleanup_scheduler(self):
        if self._thread and self._thread.is_alive():
            return  # already running
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._thread.start()

    def stop_cleanup_scheduler(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join()
            self._thread = None

    def _cleanup_loop(self):
        # Run cleanup immediately on start
        self.cleanup_old_logs()
        while not self._stop_event.is_set():
            # Wait for the next interval or until stopped
            if self._stop_event.wait(self.cleanup_interval_hours * 3600):
                break
            self.cleanup_old_logs()

    def cleanup_old_logs(self):
        if not self.log_dir.is_dir():
            return

        cutoff = datetime.now() - timedelta(days=self.max_age_days)
        files_deleted = 0
        bytes_freed = 0

        for entry in self.log_dir.iterdir():
            if not entry.is_file():
                continue
            try:
                mtime = datetime.fromtimestamp(entry.stat().st_mtime)
            except OSError:
                continue
            if mtime < cutoff:
                try:
                    size = entry.stat().st_size
                    entry.unlink()
                    files_deleted += 1
                    bytes_freed += size
                except OSError:
                    continue

        with self._lock:
            self._last_cleanup_time = datetime.now()
            self._files_deleted = files_deleted
            self._bytes_freed = bytes_freed

    def get_cleanup_stats(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "last_cleanup_time": self._last_cleanup_time,
                "files_deleted": self._files_deleted,
                "bytes_freed": self._bytes_freed,
            }
