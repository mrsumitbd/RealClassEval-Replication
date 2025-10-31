
import logging
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
        self.logger = logging.getLogger(__name__)

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        '''
        Centralized error handling with context
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        user_message = self._get_user_friendly_message(error, context)
        self.app.notify(user_message, severity=severity)

        if severity == 'critical':
            self._report_critical_error(error, context)

        tb_str = traceback.format_exc()
        self.logger.error(f'Context: {context}\n{tb_str}')
        self._write_traceback_to_file(context, tb_str)

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        '''
        Handle errors that occur during specific operations with a standard format.
        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        context = f'Operation: {operation}'
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
        if isinstance(error, ConnectionError):
            return f'Connection issue occurred while {context}: {str(error)}'
        elif isinstance(error, PermissionError):
            return f'Permission denied while {context}: {str(error)}'
        else:
            return f'An error occurred while {context}: {str(error)}'

    def _report_critical_error(self, error: Exception, context: str) -> None:
        '''
        Report critical errors for later analysis or immediate attention.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        '''
        # Implement critical error reporting mechanism here, e.g., send email or notification
        self.logger.critical(
            f'Critical error: {context}\n{traceback.format_exc()}')

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        '''Append a timestamped traceback to the persistent error log.
        The log is stored under `logs/error.log` relative to the repository root.
        '''
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(log_dir, 'error.log')
        with open(log_file, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'{timestamp}\nContext: {context}\n{tb_str}\n\n')
