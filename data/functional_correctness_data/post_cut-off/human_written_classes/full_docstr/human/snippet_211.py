import os
from datetime import datetime
import traceback

class ErrorHandler:
    """
    Centralized error handling system for the PCILeech TUI application.

    This class provides a consistent way to handle errors throughout the application,
    including logging, user notifications, and critical error reporting.
    """

    def __init__(self, app):
        """
        Initialize the error handler with the app instance.

        Args:
            app: The main TUI application instance
        """
        self.app = app

    def handle_error(self, error: Exception, context: str, severity: str='error') -> None:
        """
        Centralized error handling with context

        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
            severity: Error severity level ("error", "warning", "critical")
        """
        error_msg = f'{context}: {str(error)}'
        logger.error(f'Error in {context}', exc_info=True)
        user_msg = self._get_user_friendly_message(error, context)
        self.app.notify(user_msg, severity=severity)
        try:
            tb_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            self._write_traceback_to_file(context, tb_str)
        except Exception:
            logger.exception('Failed to write traceback to error log')
        if severity == 'critical':
            self._report_critical_error(error, context)

    def handle_operation_error(self, operation: str, error: Exception, severity: str='error') -> None:
        """
        Handle errors that occur during specific operations with a standard format.

        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        """
        context = f'Failed while {operation}'
        self.handle_error(error, context, severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        """
        Generate a user-friendly error message based on the exception type and context.

        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred

        Returns:
            A user-friendly error message
        """
        error_type = type(error).__name__
        error_messages = {'FileNotFoundError': f'A required file could not be found: {str(error)}', 'PermissionError': f'Permission denied: {str(error)}. Try running with sudo.', 'ConnectionError': f'Connection failed: {str(error)}. Check network settings.', 'TimeoutError': f'Operation timed out: {str(error)}. Try again later.', 'ValueError': f'Invalid value: {str(error)}', 'NotImplementedError': f'This feature is not implemented yet: {str(error)}'}
        return error_messages.get(error_type, f'{context}: {str(error)}')

    def _report_critical_error(self, error: Exception, context: str) -> None:
        """
        Report critical errors for later analysis or immediate attention.

        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        """
        tb_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        logger.critical(f'CRITICAL ERROR in {context}: {str(error)}\n{tb_str}', exc_info=True)
        try:
            self._write_traceback_to_file(context, tb_str)
        except Exception:
            logger.exception('Failed to write critical traceback to error log')
        self.app.notify('A critical error occurred. Please save your work and restart the application.', severity='error')

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        """Append a timestamped traceback to the persistent error log.

        The log is stored under `logs/error.log` relative to the repository root.
        """
        try:
            log_dir = os.path.join(os.getcwd(), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, 'error.log')
            with open(log_path, 'a') as f:
                f.write('\n--- ERROR: ' + datetime.utcnow().isoformat() + ' UTC ---\n')
                f.write(f'Context: {context}\n')
                f.write(tb_str)
                f.write('\n')
        except Exception:
            logger.exception('Failed to persist traceback to file')