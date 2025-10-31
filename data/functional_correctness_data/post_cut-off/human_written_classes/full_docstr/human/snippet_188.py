from datetime import datetime, timedelta
import logging.handlers
import threading
import logging
import logging.config
from pathlib import Path

class LogCleanupManager:
    """Log file cleanup manager for automatic maintenance"""

    def __init__(self, log_dir: str, max_age_days: int=30, cleanup_interval_hours: int=24):
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
        self.cleanup_thread = None
        self.stop_event = threading.Event()
        self.logger = None

    def start_cleanup_scheduler(self):
        """Start the cleanup scheduler in a background thread"""
        if self.cleanup_thread and self.cleanup_thread.is_alive():
            return
        self.stop_event.clear()
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
        if not self.logger:
            self.logger = logging.getLogger('doris_mcp_server.log_cleanup')
        self.logger.info(f'Log cleanup scheduler started - cleanup every {self.cleanup_interval_hours}h, max age {self.max_age_days} days')

    def stop_cleanup_scheduler(self):
        """Stop the cleanup scheduler"""
        if self.cleanup_thread and self.cleanup_thread.is_alive():
            self.stop_event.set()
            self.cleanup_thread.join(timeout=5)
            if self.logger:
                self.logger.info('Log cleanup scheduler stopped')

    def _cleanup_loop(self):
        """Background loop for periodic cleanup"""
        while not self.stop_event.is_set():
            try:
                self.cleanup_old_logs()
                for _ in range(self.cleanup_interval_hours * 60):
                    if self.stop_event.wait(60):
                        break
            except Exception as e:
                if self.logger:
                    self.logger.error(f'Error in log cleanup loop: {e}')
                self.stop_event.wait(300)

    def cleanup_old_logs(self):
        """Clean up old log files based on age"""
        if not self.log_dir.exists():
            return
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(days=self.max_age_days)
        cleaned_files = []
        cleaned_size = 0
        log_patterns = ['doris_mcp_server_*.log', 'doris_mcp_server_*.log.*']
        for pattern in log_patterns:
            for log_file in self.log_dir.glob(pattern):
                try:
                    file_mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if file_mtime < cutoff_time:
                        file_size = log_file.stat().st_size
                        log_file.unlink()
                        cleaned_files.append(log_file.name)
                        cleaned_size += file_size
                except Exception as e:
                    if self.logger:
                        self.logger.warning(f'Failed to cleanup log file {log_file}: {e}')
        if cleaned_files and self.logger:
            size_mb = cleaned_size / (1024 * 1024)
            self.logger.info(f'Cleaned up {len(cleaned_files)} old log files, freed {size_mb:.2f} MB')
            self.logger.debug(f"Cleaned files: {', '.join(cleaned_files)}")

    def get_cleanup_stats(self) -> dict:
        """Get statistics about log files and cleanup status"""
        if not self.log_dir.exists():
            return {'error': 'Log directory does not exist'}
        stats = {'log_directory': str(self.log_dir.absolute()), 'max_age_days': self.max_age_days, 'cleanup_interval_hours': self.cleanup_interval_hours, 'scheduler_running': self.cleanup_thread and self.cleanup_thread.is_alive(), 'total_files': 0, 'total_size_mb': 0, 'files_by_age': {'recent': 0, 'old': 0}, 'oldest_file': None, 'newest_file': None}
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(days=self.max_age_days)
        oldest_time = None
        newest_time = None
        log_patterns = ['doris_mcp_server_*.log', 'doris_mcp_server_*.log.*']
        for pattern in log_patterns:
            for log_file in self.log_dir.glob(pattern):
                try:
                    file_stat = log_file.stat()
                    file_mtime = datetime.fromtimestamp(file_stat.st_mtime)
                    stats['total_files'] += 1
                    stats['total_size_mb'] += file_stat.st_size / (1024 * 1024)
                    if file_mtime < cutoff_time:
                        stats['files_by_age']['old'] += 1
                    else:
                        stats['files_by_age']['recent'] += 1
                    if oldest_time is None or file_mtime < oldest_time:
                        oldest_time = file_mtime
                        stats['oldest_file'] = {'name': log_file.name, 'age_days': (current_time - file_mtime).days}
                    if newest_time is None or file_mtime > newest_time:
                        newest_time = file_mtime
                        stats['newest_file'] = {'name': log_file.name, 'age_days': (current_time - file_mtime).days}
                except Exception:
                    continue
        stats['total_size_mb'] = round(stats['total_size_mb'], 2)
        return stats