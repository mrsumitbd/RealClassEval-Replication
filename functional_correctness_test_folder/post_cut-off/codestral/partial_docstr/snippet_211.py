
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
        self.logger = logging.getLogger('PCILeechTUI')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('pci_leech_tui.log')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        '''
        Handle errors with a given context and severity level.
        Args:
            error: The exception that occurred
            context: The context in which the error occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        user_message = self._get_user_friendly_message(error, context)
        self.app.show_message(user_message, severity)

        if severity == 'critical':
            self._report_critical_error(error, context)

        log_message = f"{context}: {str(error)}"
        if severity == 'error':
            self.logger.error(log_message)
        elif severity == 'warning':
            self.logger.warning(log_message)
        elif severity == 'critical':
            self.logger.critical(log_message)

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
        '''
        Generate a user-friendly message based on the error and context.
        Args:
            error: The exception that occurred
            context: The context in which the error occurred
        Returns:
            str: A user-friendly error message
        '''
        error_type = type(error).__name__
        if error_type == 'FileNotFoundError':
            return f"File not found: {error.filename}"
        elif error_type == 'PermissionError':
            return f"Permission denied: {error.filename}"
        elif error_type == 'OSError':
            return f"Operating system error: {error.strerror}"
        else:
            return f"An error occurred: {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        '''
        Report a critical error to the user and write the traceback to a file.
        Args:
            error: The exception that occurred
            context: The context in which the error occurred
        '''
        tb_str = traceback.format_exc()
        self._write_traceback_to_file(context, tb_str)
        self.app.show_message(
            f"A critical error occurred and has been reported. Please check the log file for details.", 'critical')

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        '''
        Write the traceback to a file with a timestamp.
        Args:
            context: The context in which the error occurred
            tb_str: The traceback string
        '''
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"critical_error_{timestamp}.log"
        with open(filename, 'w') as f:
            f.write(f"Context: {context}\n")
            f.write(tb_str)
