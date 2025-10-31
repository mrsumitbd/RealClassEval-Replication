
import os
import time
import logging
import schedule
import threading
from datetime import datetime, timedelta


class LogCleanupManager:

    def __init__(self, log_dir: str, max_age_days: int = 30, cleanup_interval_hours: int = 24):
        self.log_dir = log_dir
        self.max_age_days = max_age_days
        self.cleanup_interval_hours = cleanup_interval_hours
        self.cleanup_stats = {'deleted_files': 0, 'total_size': 0}
        self.scheduler_running = False
        self.logger = logging.getLogger(__name__)

    def start_cleanup_scheduler(self):
        if not self.scheduler_running:
            self.scheduler_running = True
            schedule.every(self.cleanup_interval_hours).hours.do(
                self._cleanup_loop)
            threading.Thread(target=self._run_scheduler).start()
            self.logger.info("Log cleanup scheduler started.")

    def stop_cleanup_scheduler(self):
        self.scheduler_running = False
        self.logger.info("Log cleanup scheduler stopped.")

    def _cleanup_loop(self):
        self.cleanup_old_logs()

    def _run_scheduler(self):
        while self.scheduler_running:
            schedule.run_pending()
            time.sleep(1)

    def cleanup_old_logs(self):
        cutoff_date = datetime.now() - timedelta(days=self.max_age_days)
        for filename in os.listdir(self.log_dir):
            filepath = os.path.join(self.log_dir, filename)
            if os.path.isfile(filepath):
                file_mod_time = datetime.fromtimestamp(
                    os.path.getmtime(filepath))
                if file_mod_time < cutoff_date:
                    try:
                        file_size = os.path.getsize(filepath)
                        os.remove(filepath)
                        self.cleanup_stats['deleted_files'] += 1
                        self.cleanup_stats['total_size'] += file_size
                        self.logger.info(f"Deleted log file: {filename}")
                    except Exception as e:
                        self.logger.error(
                            f"Failed to delete log file: {filename}. Error: {str(e)}")

    def get_cleanup_stats(self) -> dict:
        return self.cleanup_stats.copy()
