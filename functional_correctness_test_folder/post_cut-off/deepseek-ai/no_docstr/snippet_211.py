
class ErrorHandler:

    def __init__(self, app):
        self.app = app

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        message = self._get_user_friendly_message(error, context)
        if severity == 'critical':
            self._report_critical_error(error, context)
        print(f"{severity.upper()}: {message}")
        self._write_traceback_to_file(context, str(error))

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        context = f"Operation: {operation}"
        self.handle_error(error, context, severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        return f"An error occurred in {context}: {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        print(f"CRITICAL ERROR REPORTED: {context} - {str(error)}")

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        with open("error_log.txt", "a") as f:
            f.write(f"Context: {context}\nTraceback: {tb_str}\n\n")
