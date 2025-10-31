
import traceback
import datetime
import os


class ErrorHandler:

    def __init__(self, app):
        self.app = app
        self.log_dir = getattr(app, 'log_dir', 'logs')
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        msg = self._get_user_friendly_message(error, context)
        tb_str = ''.join(traceback.format_exception(
            type(error), error, error.__traceback__))
        if severity == 'critical':
            self._report_critical_error(error, context)
        self._write_traceback_to_file(context, tb_str)
        if hasattr(self.app, 'logger'):
            log_func = getattr(self.app.logger, severity,
                               self.app.logger.error)
            log_func(f"{context}: {msg}")
        else:
            print(f"[{severity.upper()}] {context}: {msg}")

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        context = f"Operation '{operation}'"
        self.handle_error(error, context, severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        if isinstance(error, FileNotFoundError):
            return f"Required file not found during {context}."
        elif isinstance(error, ValueError):
            return f"Invalid value encountered during {context}."
        elif isinstance(error, PermissionError):
            return f"Permission denied during {context}."
        else:
            return f"An unexpected error occurred during {context}: {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        # Placeholder for reporting, e.g., sending an email or alert
        if hasattr(self.app, 'notify_admin'):
            self.app.notify_admin(f"Critical error in {context}: {str(error)}")
        else:
            print(f"[CRITICAL REPORT] {context}: {str(error)}")

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_context = "".join(c if c.isalnum() or c in (
            ' ', '_') else '_' for c in context)
        filename = f"{self.log_dir}/error_{safe_context}_{timestamp}.log"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Context: {context}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write("Traceback:\n")
            f.write(tb_str)
