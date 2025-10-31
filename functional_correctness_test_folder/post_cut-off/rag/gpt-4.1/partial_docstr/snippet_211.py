import os
import sys
import traceback
import datetime


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

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        '''
        Centralized error handling with context
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        tb_str = ''.join(traceback.format_exception(
            type(error), error, error.__traceback__))
        user_msg = self._get_user_friendly_message(error, context)
        # Log to file
        self._write_traceback_to_file(context, tb_str)
        # Notify user
        if hasattr(self.app, 'notify_user'):
            self.app.notify_user(user_msg, severity)
        else:
            print(f"[{severity.upper()}] {user_msg}", file=sys.stderr)
        # If critical, report
        if severity == 'critical':
            self._report_critical_error(error, context)

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        '''
        Handle errors that occur during specific operations with a standard format.
        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        context = f"Error during operation: {operation}"
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
        if isinstance(error, FileNotFoundError):
            return f"{context}: File not found ({error.filename})"
        elif isinstance(error, PermissionError):
            return f"{context}: Permission denied ({error.filename})"
        elif isinstance(error, ValueError):
            return f"{context}: Invalid value - {str(error)}"
        elif isinstance(error, OSError):
            return f"{context}: OS error - {str(error)}"
        elif isinstance(error, KeyboardInterrupt):
            return f"{context}: Operation cancelled by user."
        else:
            return f"{context}: {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        '''
        Report critical errors for later analysis or immediate attention.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        '''
        # For now, just print to stderr and log. Could be extended to send to remote server.
        tb_str = ''.join(traceback.format_exception(
            type(error), error, error.__traceback__))
        critical_msg = f"CRITICAL ERROR: {context}\n{str(error)}"
        print(critical_msg, file=sys.stderr)
        self._write_traceback_to_file(context, tb_str)
        if hasattr(self.app, 'notify_user'):
            self.app.notify_user(
                "A critical error occurred. Please check the error log.", "critical")

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        '''Append a timestamped traceback to the persistent error log.
        The log is stored under `logs/error.log` relative to the repository root.
        '''
        log_dir = os.path.join(os.path.dirname(
            os.path.abspath(sys.argv[0])), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "error.log")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n[{timestamp}] {context}\n")
            f.write(tb_str)
            f.write("\n" + ("-"*80) + "\n")
