
import os
import time
import threading
from datetime import datetime, timedelta


class LogCleanupManager:

    def __init__(self, log_dir: str, max_age_days: int = 30, cleanup_interval_hours: int = 24):
        '''
        Initialize log cleanup manager.
        Args:
            log_dir: Directory containing log files
            max_age_days: Maximum age of log files in days (default: 30 days)
            cleanup_interval_hours: Cleanup interval in hours (default: 24 hours)
        '''
        self.log_dir = log_dir
        self.max_age_days = max_age_days
        self.cleanup_interval_hours = cleanup_interval_hours
        self.cleanup_scheduler_running = False
        self.stats = {'total_logs': 0, 'deleted_logs': 0, 'last_cleanup': None}

    def start_cleanup_scheduler(self):
        '''Start the cleanup scheduler in a background thread'''
        if not self.cleanup_scheduler_running:
            self.cleanup_scheduler_running = True
            self.cleanup_thread = threading.Thread(target=self._cleanup_loop)
            self.cleanup_thread.daemon = True
            self.cleanup_thread.start()

    def stop_cleanup_scheduler(self):
        '''Stop the cleanup scheduler'''
        self.cleanup_scheduler_running = False

    def _cleanup_loop(self):
        while self.cleanup_scheduler_running:
            self.cleanup_old_logs()
            time.sleep(self.cleanup_interval_hours * 3600)

    def cleanup_old_logs(self):
        '''Clean up old log files based on age'''
        cutoff_date = datetime.now() - timedelta(days=self.max_age_days)
        deleted_count = 0
        total_count = 0
        for filename in os.listdir(self.log_dir):
            filepath = os.path.join(self.log_dir, filename)
            if os.path.isfile(filepath):
                total_count += 1
                file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if file_mtime < cutoff_date:
                    try:
                        os.remove(filepath)
                        deleted_count += 1
                    except Exception as e:
                        print(f"Error deleting log file {filename}: {str(e)}")
        self.stats['total_logs'] = total_count
        self.stats['deleted_logs'] = deleted_count
        self.stats['last_cleanup'] = datetime.now()

    def get_cleanup_stats(self) -> dict:
        '''Get statistics about log files and cleanup status'''
        return self.stats


# Example usage:
if __name__ == "__main__":
    log_dir = "/path/to/log/dir"
    log_cleanup_manager = LogCleanupManager(log_dir)
    log_cleanup_manager.start_cleanup_scheduler()
    try:
        while True:
            time.sleep(1)
            stats = log_cleanup_manager.get_cleanup_stats()
            print(stats)
    except KeyboardInterrupt:
        log_cleanup_manager.stop_cleanup_scheduler()
