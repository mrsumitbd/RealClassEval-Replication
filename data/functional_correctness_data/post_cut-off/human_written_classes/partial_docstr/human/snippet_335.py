from rich.logging import RichHandler
from rich.console import Console
import sys
import logging
import os

class LoggingManager:

    def __init__(self, command_type, layout=None, live=None):
        self.command_type = command_type
        self.layout = layout
        self.live = live
        self.delayed_handler = None
        self.init_logging()

    def init_logging(self):
        """Initialize logging based on command type."""
        log_level = os.getenv('GENAI_BENCH_LOGGING_LEVEL', 'INFO').upper()
        enable_ui = os.getenv('ENABLE_UI', 'true').lower() == 'true'
        if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            log_level = 'INFO'
        file_handler = self.get_file_handler()
        if self.command_type == 'benchmark':
            extra_handlers = self.init_ui_logging() if enable_ui else [self.get_console_handler()]
        else:
            extra_handlers = [self.get_rich_handler()]
        logging.basicConfig(level=log_level, handlers=[file_handler, *extra_handlers])
        self.setup_exception_handler()

    def setup_exception_handler(self):
        """Set up exception handling to log uncaught exceptions."""

        def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                if self.delayed_handler:
                    self.delayed_handler.flush_buffer()
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            logging.error('Uncaught exception', exc_info=(exc_type, exc_value, exc_traceback))
            if self.delayed_handler:
                self.delayed_handler.flush_buffer()
            sys.exit(1)
        sys.excepthook = handle_uncaught_exception

    @staticmethod
    def get_file_handler():
        """Return a file handler for logging."""
        file_log_format = '{levelname:<8} {asctime} - {name}:{funcName} - {message}'
        date_format = '%Y-%m-%d %H:%M:%S.%f'
        file_handler = logging.FileHandler('genai_bench.log')
        file_formatter = logging.Formatter(file_log_format, datefmt=date_format, style='{')
        file_handler.setFormatter(file_formatter)
        return file_handler

    @staticmethod
    def get_console_handler():
        """Return a console handler for logging with a standard format."""
        log_format = '{levelname:<8} {asctime} - {name}:{funcName} - {message}'
        date_format = '%Y-%m-%d %H:%M:%S.%f'
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(log_format, datefmt=date_format, style='{')
        console_handler.setFormatter(console_formatter)
        return console_handler

    @staticmethod
    def get_rich_handler():
        """Return a rich handler for logging."""
        rich_handler = RichHandler(rich_tracebacks=True)
        rich_formatter = logging.Formatter('%(message)s', style='%')
        rich_handler.setFormatter(rich_formatter)
        return rich_handler

    def init_ui_logging(self):
        """Initialize UI logging handlers for 'benchmark'."""
        date_format = '%Y-%m-%d %H:%M:%S.%f'
        panel_handler = RollingRichPanelHandler(layout=self.layout, rich_tracebacks=True, log_time_format=date_format)
        panel_formatter = logging.Formatter('%(message)s', datefmt=date_format, style='%')
        panel_handler.setFormatter(panel_formatter)
        self.delayed_handler = DelayedRichHandler(live=self.live, console=Console(), rich_tracebacks=True)
        delayed_formatter = logging.Formatter('%(message)s', style='%')
        self.delayed_handler.setFormatter(delayed_formatter)
        return [panel_handler, self.delayed_handler]