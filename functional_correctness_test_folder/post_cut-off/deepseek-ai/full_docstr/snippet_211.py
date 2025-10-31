
import traceback
from datetime import datetime
import os


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
        self.log_dir = "logs"
        self.log_file = os.path.join(self.log_dir, "error.log")
        os.makedirs(self.log_dir, exist_ok=True)

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        '''
        Centralized error handling with context
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        tb_str = traceback.format_exc()
        self._write_traceback_to_file(context, tb_str)
        message = self._get_user_friendly_message(error, context)

        if severity == 'critical':
            self._report_critical_error(error, context)

        if hasattr(self.app, 'show_error'):
            self.app.show_error(message, severity)

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        '''
        Handle errors that occur during specific operations with a standard format.
        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        context = f"Operation failed: {operation}"
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
        return f"{context}: {error_type} - {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        '''
        Report critical errors for later analysis or immediate attention.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        '''
        # Placeholder for critical error reporting (e.g., send to server, notify admin)
        pass

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        '''Append a timestamped traceback to the persistent error log.
        The log is stored under `logs/error.log` relative to the repository root.
        '''
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {context}\n{tb_str}\n{'='*50}\n"

        with open(self.log_file, 'a') as f:
            f.write(log_entry)
