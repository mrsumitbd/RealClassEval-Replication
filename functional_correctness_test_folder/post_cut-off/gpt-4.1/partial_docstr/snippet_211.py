
import logging
import traceback
import datetime
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
        self.logger = logging.getLogger("PCILeechTUI")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        msg = self._get_user_friendly_message(error, context)
        tb_str = ''.join(traceback.format_exception(
            type(error), error, error.__traceback__))
        if severity == 'critical':
            self.logger.critical(f"{context}: {msg}\n{tb_str}")
            self._report_critical_error(error, context)
        elif severity == 'warning':
            self.logger.warning(f"{context}: {msg}")
        else:
            self.logger.error(f"{context}: {msg}")
        # Notify user via app (if possible)
        if hasattr(self.app, 'notify_user'):
            self.app.notify_user(msg, severity)
        # For critical errors, write traceback to file
        if severity == 'critical':
            self._write_traceback_to_file(context, tb_str)

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
        # Customize for known error types if needed
        if isinstance(error, FileNotFoundError):
            return f"{context}: File not found ({error.filename})"
        elif isinstance(error, PermissionError):
            return f"{context}: Permission denied ({error.filename})"
        elif isinstance(error, ValueError):
            return f"{context}: Invalid value - {str(error)}"
        else:
            return f"{context}: {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        # For now, just log and notify user. Could be extended to send reports.
        msg = f"Critical error occurred: {context}. Please check the log file for details."
        if hasattr(self.app, 'notify_user'):
            self.app.notify_user(msg, 'critical')

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        # Write the traceback to a file with timestamp
        log_dir = getattr(self.app, 'log_dir', '.')
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except Exception:
                log_dir = '.'
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_context = "".join(c if c.isalnum() or c in (
            ' ', '_') else '_' for c in context)
        filename = f"critical_error_{safe_context}_{timestamp}.log"
        filepath = os.path.join(log_dir, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Context: {context}\n")
                f.write(tb_str)
        except Exception as e:
            self.logger.error(f"Failed to write critical error log: {e}")
