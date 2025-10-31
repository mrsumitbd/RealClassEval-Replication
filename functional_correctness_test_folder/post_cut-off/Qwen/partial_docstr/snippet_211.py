
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
        handler = logging.FileHandler('error_log.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        user_friendly_message = self._get_user_friendly_message(error, context)
        self.logger.log(self._get_logging_level(severity),
                        f"{context}: {user_friendly_message}")
        if severity == 'critical':
            self._report_critical_error(error, context)
        self.app.notify_user(user_friendly_message)

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        '''
        Handle errors that occur during specific operations with a standard format.
        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        context = f"Error during {operation}"
        self.handle_error(error, context, severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        return f"An error occurred in {context}: {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        tb_str = traceback.format_exc()
        self._write_traceback_to_file(context, tb_str)
        self.app.notify_user(
            f"Critical error in {context}: {str(error)}. Check error_log.log for details.")

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        with open(f"traceback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", 'w') as f:
            f.write(f"Context: {context}\n")
            f.write(tb_str)

    def _get_logging_level(self, severity: str) -> int:
        levels = {
            'error': logging.ERROR,
            'warning': logging.WARNING,
            'critical': logging.CRITICAL
        }
        return levels.get(severity, logging.ERROR)
