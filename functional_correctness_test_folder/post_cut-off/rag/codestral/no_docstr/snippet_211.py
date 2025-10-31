
import logging
import traceback
from datetime import datetime
from pathlib import Path


class ErrorHandler:
    '''
    Centralized error handling system for the PCILeech TUI application.
    This class provides a consistent way to handle errors throughout the application,
    including logging, user notifications, and critical error reporting.
    '''

    def __init__(self, app):
        '''
        Initialize the error handler with the app instance.
        Args:
            app: The main TUI application instance
        '''
        self.app = app
        self.logger = logging.getLogger('PCILeech')
        self.error_log_path = Path(
            __file__).parent.parent / 'logs' / 'error.log'
        self.error_log_path.parent.mkdir(parents=True, exist_ok=True)

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        '''
        Centralized error handling with context
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        user_message = self._get_user_friendly_message(error, context)
        self.logger.error(f"{severity.upper()}: {user_message}")

        if severity == 'critical':
            self._report_critical_error(error, context)

        if self.app:
            self.app.notify(f"[ERROR] {user_message}", severity=severity)

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        '''
        Handle errors that occur during specific operations with a standard format.
        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        context = f"During {operation}"
        self.handle_error(error, context, severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        '''
        Generate a user-friendly error message based on the exception type and context.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        Returns:
            A user-friendly error message
        '''
        error_type = type(error).__name__
        error_msg = str(error)

        if error_type == 'FileNotFoundError':
            return f"File not found: {error_msg} {context}"
        elif error_type == 'PermissionError':
            return f"Permission denied: {error_msg} {context}"
        elif error_type == 'ConnectionError':
            return f"Connection failed: {error_msg} {context}"
        else:
            return f"An error occurred {context}: {error_msg}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        '''
        Report critical errors for later analysis or immediate attention.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        '''
        tb_str = traceback.format_exc()
        self._write_traceback_to_file(context, tb_str)
        self.logger.critical(f"CRITICAL ERROR: {context}\n{tb_str}")

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        '''Append a timestamped traceback to the persistent error log.
        The log is stored under `logs/error.log` relative to the repository root.
        '''
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {context}\n{tb_str}\n{'='*80}\n"

        with open(self.error_log_path, 'a') as f:
            f.write(log_entry)
