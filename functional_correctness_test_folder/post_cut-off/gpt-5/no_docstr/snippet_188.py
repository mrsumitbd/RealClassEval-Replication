import os
import threading
import time
from pathlib import Path
from typing import Optional, Dict


class LogCleanupManager:

    def __init__(self, log_dir: str, max_age_days: int = 30, cleanup_interval_hours: int = 24):
        self.log_dir = Path(log_dir)
        self.max_age_days = max(0, int(max_age_days))
        self.cleanup_interval_hours = max(1, int(cleanup_interval_hours))
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._stats: Dict[str, Optional[object]] = {
            "last_cleanup_time": None,
            "last_run_duration_seconds": None,
            "files_deleted_count": 0,
            "total_deleted_bytes": 0,
            "runs_count": 0,
            "last_error": None,
            "scheduler_running": False,
        }
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            with self._lock:
                self._stats["last_error"] = f"Failed to ensure log directory exists: {e}"

    def start_cleanup_scheduler(self):
        with self._lock:
            if self._thread and self._thread.is_alive():
                return
            self._stop_event.clear()
            self._stats["scheduler_running"] = True
            self._thread = threading.Thread(
                target=self._cleanup_loop, name="LogCleanupManager", daemon=True)
            self._thread.start()

    def stop_cleanup_scheduler(self):
        thread_to_join = None
        with self._lock:
            if self._thread and self._thread.is_alive():
                self._stop_event.set()
                thread_to_join = self._thread
            self._stats["scheduler_running"] = False
        if thread_to_join:
            thread_to_join.join(timeout=self.cleanup_interval_hours * 3600 + 5)

    def _cleanup_loop(self):
        try:
            while not self._stop_event.is_set():
                self.cleanup_old_logs()
                if self._stop_event.wait(self.cleanup_interval_hours * 3600):
                    break
        finally:
            with self._lock:
                self._stats["scheduler_running"] = False

    def cleanup_old_logs(self):
        start = time.time()
        files_deleted = 0
        bytes_deleted = 0
        last_error = None

        cutoff_ts = start - (self.max_age_days * 86400)

        try:
            if not self.log_dir.exists():
                self.log_dir.mkdir(parents=True, exist_ok=True)

            for root, dirs, files in os.walk(self.log_dir, followlinks=False):
                for fname in files:
                    fpath = Path(root) / fname
                    try:
                        # Skip if not a regular file
                        try:
                            st = fpath.lstat()
                        except FileNotFoundError:
                            continue
                        if not fpath.is_file() and not (os.path.isfile(fpath)):
                            continue

                        mtime = st.st_mtime
                        if mtime <= cutoff_ts:
                            size = st.st_size
                            try:
                                fpath.unlink(missing_ok=False)
                                files_deleted += 1
                                bytes_deleted += size
                            except FileNotFoundError:
                                continue
                            except PermissionError as pe:
                                last_error = f"Permission error deleting {fpath}: {pe}"
                            except Exception as e:
                                last_error = f"Error deleting {fpath}: {e}"
                    except Exception as e:
                        last_error = f"Error processing {fpath}: {e}"
        except Exception as e:
            last_error = f"Cleanup iteration failed: {e}"

        duration = time.time() - start
        with self._lock:
            self._stats["last_cleanup_time"] = time.time()
            self._stats["last_run_duration_seconds"] = duration
            self._stats["files_deleted_count"] = self._stats.get(
                "files_deleted_count", 0) + files_deleted
            self._stats["total_deleted_bytes"] = self._stats.get(
                "total_deleted_bytes", 0) + bytes_deleted
            self._stats["runs_count"] = self._stats.get("runs_count", 0) + 1
            if last_error:
                self._stats["last_error"] = last_error

    def get_cleanup_stats(self) -> dict:
        with self._lock:
            return dict(self._stats)
