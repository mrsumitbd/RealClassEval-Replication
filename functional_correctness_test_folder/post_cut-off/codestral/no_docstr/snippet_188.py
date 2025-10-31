
import os
import time
import threading
from datetime import datetime, timedelta


class LogCleanupManager:

    def __init__(self, log_dir: str, max_age_days: int = 30, cleanup_interval_hours: int = 24):

        self.log_dir = log_dir
        self.max_age_days = max_age_days
        self.cleanup_interval_hours = cleanup_interval_hours
        self.cleanup_stats = {
            'last_cleanup_time': None,
            'total_files_deleted': 0,
            'total_space_freed': 0
        }
        self.scheduler = None
        self.running = False

    def start_cleanup_scheduler(self):

        if not self.running:
            self.running = True
            self.scheduler = threading.Thread(target=self._cleanup_loop)
            self.scheduler.start()

    def stop_cleanup_scheduler(self):

        if self.running:
            self.running = False
            if self.scheduler:
                self.scheduler.join()

    def _cleanup_loop(self):

        while self.running:
            self.cleanup_old_logs()
            time.sleep(self.cleanup_interval_hours * 3600)

    def cleanup_old_logs(self):

        now = datetime.now()
        cutoff_time = now - timedelta(days=self.max_age_days)
        files_deleted = 0
        space_freed = 0

        for root, dirs, files in os.walk(self.log_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_mtime = datetime.fromtimestamp(
                    os.path.getmtime(file_path))
                if file_mtime < cutoff_time:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    files_deleted += 1
                    space_freed += file_size

        self.cleanup_stats['last_cleanup_time'] = now
        self.cleanup_stats['total_files_deleted'] += files_deleted
        self.cleanup_stats['total_space_freed'] += space_freed

    def get_cleanup_stats(self) -> dict:

        return self.cleanup_stats
