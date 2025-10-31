
import traceback
from datetime import datetime


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
        self.log_file = "error_log.txt"

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        '''
        Handle a general error with logging and user notification.
        Args:
            error: The exception that occurred
            context: Contextual information about where the error occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        tb_str = traceback.format_exc()
        self._write_traceback_to_file(context, tb_str)
        message = self._get_user_friendly_message(error, context)

        if severity == 'critical':
            self._report_critical_error(error, context)

        if hasattr(self.app, 'notify_user'):
            self.app.notify_user(f"{severity.upper()}: {message}")

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        '''
        Handle errors that occur during specific operations with a standard format.
        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        context = f"Operation: {operation}"
        self.handle_error(error, context, severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        '''
        Generate a user-friendly error message.
        Args:
            error: The exception that occurred
            context: Contextual information about where the error occurred
        Returns:
            str: A user-friendly error message
        '''
        return f"{context}: {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        '''
        Report a critical error, potentially halting the application.
        Args:
            error: The exception that occurred
            context: Contextual information about where the error occurred
        '''
        if hasattr(self.app, 'shutdown'):
            self.app.shutdown(f"Critical error in {context}: {str(error)}")

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        '''
        Write the traceback information to a log file.
        Args:
            context: Contextual information about where the error occurred
            tb_str: The traceback string
        '''
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] {context}\n{tb_str}\n\n")
