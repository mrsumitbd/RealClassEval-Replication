
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
        self.logger = logging.getLogger(__name__)

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        user_message = self._get_user_friendly_message(error, context)
        self.app.notify(user_message, severity=severity)
        self.logger.error(f"{context}: {str(error)}")
        if severity == 'critical':
            self._report_critical_error(error, context)
        tb_str = traceback.format_exc()
        self._write_traceback_to_file(context, tb_str)

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        '''
        Handle errors that occur during specific operations with a standard format.
        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        context = f"Operation '{operation}' failed"
        self.handle_error(error, context, severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        return f"Error in {context}: {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        # Implement critical error reporting, e.g., send to server or display a crash dialog
        self.logger.critical(f"Critical error in {context}: {str(error)}")
        self.app.notify(
            f"Critical error: {context}. Please report this issue.", severity='critical')

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"crash_{timestamp}.log"
        with open(filename, 'w') as f:
            f.write(f"Context: {context}\n")
            f.write(tb_str)
        self.logger.info(f"Traceback written to {filename}")
