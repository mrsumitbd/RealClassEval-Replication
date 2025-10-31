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
        user_msg = self._get_user_friendly_message(error, context)
        tb_str = ''.join(traceback.format_exception(
            type(error), error, error.__traceback__))
        # Log to file
        self._write_traceback_to_file(context, tb_str)
        # Notify user
        if hasattr(self.app, "notify_error"):
            self.app.notify_error(user_msg, severity=severity)
        elif hasattr(self.app, "show_message"):
            self.app.show_message(user_msg)
        else:
            print(f"[{severity.upper()}] {user_msg}", file=sys.stderr)
        # If critical, report
        if severity == "critical":
            self._report_critical_error(error, context)

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        '''
        Handle errors that occur during specific operations with a standard format.
        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        context = f"While {operation}"
        self.handle_error(error, context, severity=severity)

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
            return f"{context}: File not found: {error.filename}"
        elif isinstance(error, PermissionError):
            return f"{context}: Permission denied: {error.filename}"
        elif isinstance(error, ValueError):
            return f"{context}: Invalid value: {str(error)}"
        elif isinstance(error, OSError):
            return f"{context}: OS error: {str(error)}"
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
        # For now, just log to file and print to stderr.
        tb_str = ''.join(traceback.format_exception(
            type(error), error, error.__traceback__))
        self._write_traceback_to_file(context, tb_str)
        msg = f"CRITICAL ERROR reported: {context}\n{str(error)}"
        if hasattr(self.app, "notify_critical"):
            self.app.notify_critical(msg)
        else:
            print(msg, file=sys.stderr)

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
            f.write("\n" + ("-"*60) + "\n")
