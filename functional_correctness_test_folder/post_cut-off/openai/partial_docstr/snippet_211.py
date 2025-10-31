
import logging
import os
import sys
import traceback
from datetime import datetime
from typing import Optional


class ErrorHandler:
    """
    Centralized error handling system for the PCILeech TUI application.
    This class provides a consistent way to handle errors throughout the application,
    including logging, user notifications, and critical error reporting.
    """

    def __init__(self, app):
        """
        Initialize the error handler with the app instance.
        Args:
            app: The main TUI application instance
        """
        self.app = app
        self.logger = logging.getLogger("PCILeechErrorHandler")
        self.logger.setLevel(logging.DEBUG)

        # Ensure logs directory exists
        self.log_dir = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "logs")
        os.makedirs(self.log_dir, exist_ok=True)

        # File handler for all logs
        log_file = os.path.join(self.log_dir, "error_handler.log")
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        fh.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(fh)

    def handle_error(self, error: Exception, context: str, severity: str = "error") -> None:
        """
        Handle a generic error.
        """
        try:
            # Log the error
            tb_str = "".join(traceback.format_exception(
                type(error), error, error.__traceback__))
            self.logger.log(self._severity_to_level(severity),
                            f"{context}: {error}\n{tb_str}")

            # Write traceback to file
            self._write_traceback_to_file(context, tb_str)

            # Get user-friendly message
            user_msg = self._get_user_friendly_message(error, context)

            # Notify user
            self._notify_user(user_msg, severity)

            # If critical, report and exit
            if severity.lower() == "critical":
                self._report_critical_error(error, context)
        except Exception as e:
            # If error handling itself fails, log to stderr
            sys.stderr.write(f"ErrorHandler failed: {e}\n")
            sys.stderr.flush()

    def handle_operation_error(
        self, operation: str, error: Exception, severity: str = "error"
    ) -> None:
        """
        Handle errors that occur during specific operations with a standard format.
        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        """
        context = f"Operation '{operation}'"
        self.handle_error(error, context, severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        """
        Generate a user-friendly error message based on the exception type.
        """
        if isinstance(error, FileNotFoundError):
            return f"{context}: Required file not found. Please check the path."
        if isinstance(error, PermissionError):
            return f"{context}: Permission denied. Run with appropriate privileges."
        if isinstance(error, ConnectionError):
            return f"{context}: Network connection failed. Verify your connection."
        # Default message
        return f"{context}: An unexpected error occurred: {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        """
        Report a critical error: log, notify user, and exit the application.
        """
        self.logger.critical(f"Critical error in {context}: {error}")
        # Notify user about critical failure
        self._notify_user(
            f"Critical error: {context}. The application will exit.", "critical"
        )
        # Exit after a short delay to allow user to read message
        try:
            import time

            time.sleep(2)
        finally:
            sys.exit(1)

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        """
        Write the traceback string to a timestamped file in the logs directory.
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        safe_context = "".join(c if c.isalnum() else "_" for c in context)
        filename = f"traceback_{safe_context}_{timestamp}.log"
        filepath = os.path.join(self.log_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(tb_str)

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def _severity_to_level(self, severity: str) -> int:
        """
        Convert severity string to logging level.
        """
        sev = severity.lower()
        if sev == "critical":
            return logging.CRITICAL
        if sev == "error":
            return logging.ERROR
        if sev == "warning":
            return logging.WARNING
        if sev == "info":
            return logging.INFO
        return logging.ERROR

    def _notify_user(self, message: str, severity: str) -> None:
        """
        Notify the user via the application interface if available,
        otherwise fallback to console output.
        """
        # Try to use the app's notification system
        notify_methods = [
            "notify",
            "display_message",
            "show_message",
            "alert",
            "message",
        ]
        for method in notify_methods:
            if hasattr(self.app, method):
                try:
                    getattr(self.app, method)(message, severity=severity)
                    return
                except Exception:
                    # If the app's method fails, fall back to console
                    pass

        # Fallback: print to console with severity prefix
        prefix = severity.upper()
        print(f"[{prefix}] {message}", file=sys.stderr)
