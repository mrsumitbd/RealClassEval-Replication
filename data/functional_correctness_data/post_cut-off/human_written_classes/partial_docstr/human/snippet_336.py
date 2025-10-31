import multiprocessing
import os
import logging

class WorkerLoggingManager:
    """Manages logging setup for worker processes."""

    def __init__(self, worker_id: str, log_queue: multiprocessing.Queue):
        self.worker_id = worker_id
        self.log_queue = log_queue
        self.setup_logging()

    def setup_logging(self):
        """Set up worker-specific logging."""
        log_level = os.getenv('GENAI_BENCH_LOGGING_LEVEL', 'INFO').upper()
        file_handler = self._get_file_handler(f'genai_bench_worker_{self.worker_id}.log')
        worker_handler = self._create_worker_handler()
        logging.basicConfig(level=log_level, handlers=[file_handler, worker_handler], force=True)

    def _create_worker_handler(self) -> logging.Handler:
        """Create a rich handler that forwards logs to master."""
        handler = WorkerRichHandler(worker_id=self.worker_id, log_queue=self.log_queue, rich_tracebacks=True)
        handler.setFormatter(logging.Formatter('%(message)s', style='%'))
        return handler

    @staticmethod
    def _get_file_handler(filename: str) -> logging.FileHandler:
        """Create a file handler for worker logs."""
        file_log_format = '{levelname:<8} {asctime} - {name}:{funcName} - {message}'
        date_format = '%Y-%m-%d %H:%M:%S.%f'
        file_handler = logging.FileHandler(filename)
        file_formatter = logging.Formatter(file_log_format, datefmt=date_format, style='{')
        file_handler.setFormatter(file_formatter)
        return file_handler