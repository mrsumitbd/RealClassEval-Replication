
import logging
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
        self.logger = logging.getLogger('ErrorHandler')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('logs/error.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        '''
        Centralized error handling with context
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        tb_str = traceback.format_exc()
        user_friendly_message = self._get_user_friendly_message(error, context)
        self.logger.log(self._get_logging_level(
            severity), f'Context: {context}\nError: {error}\nTraceback: {tb_str}')
        self.app.notify(user_friendly_message)
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
        context = f'During operation: {operation}'
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
        return f'An error occurred {context}: {str(error)}'

    def _report_critical_error(self, error: Exception, context: str) -> None:
        '''
        Report critical errors for later analysis or immediate attention.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        '''
        self.logger.critical(
            f'Critical error occurred {context}: {str(error)}')
        # Additional reporting mechanisms can be added here, such as sending an email or alert

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        '''Append a timestamped traceback to the persistent error log.
        The log is stored under `logs/error.log` relative to the repository root.
        '''
        with open('logs/error.log', 'a') as log_file:
            log_file.write(
                f'{datetime.now()} - Context: {context}\nTraceback:\n{tb_str}\n')

    def _get_logging_level(self, severity: str) -> int:
        '''
        Map severity level to logging level.
        Args:
            severity: Error severity level ("error", "warning", "critical")
        Returns:
            Logging level
        '''
        severity_levels = {
            'error': logging.ERROR,
            'warning': logging.WARNING,
            'critical': logging.CRITICAL
        }
        return severity_levels.get(severity, logging.ERROR)
