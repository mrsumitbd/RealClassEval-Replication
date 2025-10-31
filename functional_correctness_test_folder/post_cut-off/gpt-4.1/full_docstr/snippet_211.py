
import os
import datetime
import traceback


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
        self.log_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'logs')
        self.log_file = os.path.join(self.log_dir, 'error.log')
        if not os.path.exists(self.log_dir):
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
        user_msg = self._get_user_friendly_message(error, context)
        # Log the error
        self._write_traceback_to_file(context, tb_str)
        # Notify user via app (if app has a notify method)
        if hasattr(self.app, 'notify'):
            self.app.notify(user_msg, severity=severity)
        # For critical errors, report
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
        context = f"Error during {operation}"
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
            return f"{context}: File not found. Please check the file path."
        elif isinstance(error, PermissionError):
            return f"{context}: Permission denied. Please check your access rights."
        elif isinstance(error, ValueError):
            return f"{context}: Invalid value encountered. Please check your input."
        elif isinstance(error, KeyboardInterrupt):
            return f"{context}: Operation cancelled by user."
        elif isinstance(error, OSError):
            return f"{context}: OS error: {str(error)}"
        else:
            return f"{context}: {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        '''
        Report critical errors for later analysis or immediate attention.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        '''
        # For now, just log with a CRITICAL tag and notify user
        tb_str = traceback.format_exc()
        critical_msg = f"CRITICAL ERROR in {context}: {str(error)}"
        self._write_traceback_to_file(context + " [CRITICAL]", tb_str)
        if hasattr(self.app, 'notify'):
            self.app.notify(critical_msg, severity='critical')
        # Optionally, could add integration with external monitoring/reporting here

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        '''Append a timestamped traceback to the persistent error log.
        The log is stored under `logs/error.log` relative to the repository root.
        '''
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = (
            f"\n[{timestamp}] {context}\n"
            f"{tb_str}\n"
            f"{'-'*60}\n"
        )
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            # If logging fails, print to stderr as last resort
            import sys
            print(f"Failed to write to error log: {e}", file=sys.stderr)
            print(log_entry, file=sys.stderr)
