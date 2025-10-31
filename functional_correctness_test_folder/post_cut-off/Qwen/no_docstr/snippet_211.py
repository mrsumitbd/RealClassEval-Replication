
import traceback
import logging


class ErrorHandler:

    def __init__(self, app):
        self.app = app
        logging.basicConfig(filename='error.log', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        user_friendly_message = self._get_user_friendly_message(error, context)
        if severity == 'critical':
            self._report_critical_error(error, context)
        logging.log(self._get_logging_level(severity),
                    f"{context}: {user_friendly_message}")
        self._write_traceback_to_file(context, traceback.format_exc())

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        context = f"Error during {operation}"
        self.handle_error(error, context, severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        return f"An error occurred in {context}: {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        logging.critical(f"Critical error in {context}: {str(error)}")
        # Additional actions for critical errors can be added here

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        with open('traceback.log', 'a') as tb_file:
            tb_file.write(f"Traceback for {context}:\n{tb_str}\n")

    def _get_logging_level(self, severity: str) -> int:
        levels = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        return levels.get(severity, logging.ERROR)
