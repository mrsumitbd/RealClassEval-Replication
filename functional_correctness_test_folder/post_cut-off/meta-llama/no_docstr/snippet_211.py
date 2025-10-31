
import logging
import traceback
from datetime import datetime


class ErrorHandler:

    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        user_friendly_message = self._get_user_friendly_message(error, context)
        self.logger.log(getattr(logging, severity.upper()),
                        user_friendly_message)
        if severity.lower() == 'critical':
            self._report_critical_error(error, context)

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        context = f"Operation '{operation}' failed"
        self.handle_error(error, context, severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        return f"Error in {context}: {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        tb_str = traceback.format_exc()
        self._write_traceback_to_file(context, tb_str)
        # Additional reporting logic can be added here (e.g., sending an email or notification)

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"error_{timestamp}.log"
        with open(filename, 'w') as f:
            f.write(f"Context: {context}\n")
            f.write(tb_str)
        self.logger.critical(f"Traceback written to {filename}")
