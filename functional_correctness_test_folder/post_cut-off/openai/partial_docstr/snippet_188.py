
import os
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any


class LogCleanupManager:
    def __init__(self, log_dir: str, max_age_days: int = 30, cleanup_interval_hours: int = 24):
        """
        Initialize log cleanup manager.

        Args:
            log_dir: Directory containing log files
            max_age_days: Maximum age of log files in days (default: 30 days)
            cleanup_interval_hours: Cleanup interval in hours (default: 24 hours)
        """
        self.log_dir = Path(log_dir)
        self.max_age_days = max_age_days
        self.cleanup_interval_hours = cleanup_interval_hours

        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()

        # Statistics
        self._stats: Dict[str, Any] = {
            "total_files": 0,
            "deleted_files": 0,
            "errors": 0,
            "last_cleanup": None,
            "running": False,
            "max_age_days": self.max_age_days,
            "cleanup_interval_hours": self.cleanup_interval_hours,
        }

    def start_cleanup_scheduler(self):
        """Start the cleanup scheduler in a background thread."""
        if self._thread and self._thread.is_alive():
            return  # already running
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._thread.start()
        with self._lock:
            self._stats["running"] = True

    def stop_cleanup_scheduler(self):
        """Stop the cleanup scheduler."""
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        with self._lock:
            self._stats["running"] = False

    def _cleanup_loop(self):
        """Internal loop that performs cleanup at the configured interval."""
        # Perform an initial cleanup immediately
        self.cleanup_old_logs()
        while not self._stop_event.is_set():
            # Sleep for the configured interval
            sleep_seconds = self.cleanup_interval_hours * 3600
            if self._stop_event.wait(timeout=sleep_seconds):
                break
            self.cleanup_old_logs()

    def cleanup_old_logs(self):
        """Clean up old log files based on age."""
        if not self.log_dir.is_dir():
            with self._lock:
                self._stats["errors"] += 1
            return

        cutoff = datetime.now() - timedelta(days=self.max_age_days)
        deleted = 0
        errors = 0
        total = 0

        for entry in self.log_dir.iterdir():
            if entry.is_file():
                total += 1
                try:
                    mtime = datetime.fromtimestamp(entry.stat().st_mtime)
                    if mtime < cutoff:
                        entry.unlink()
                        deleted += 1
                except Exception:
                    errors += 1

        with self._lock:
            self._stats.update(
                {
                    "total_files": total,
                    "deleted_files": deleted,
                    "errors": self._stats["errors"] + errors,
                    "last_cleanup": datetime.now().isoformat(),
                }
            )

    def get_cleanup_stats(self) -> dict:
        """Get statistics about log files and cleanup status."""
        with self._lock:
            return dict(self._stats)
