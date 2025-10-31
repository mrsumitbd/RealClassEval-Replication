
import os
import logging
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
        self.logger = logging.getLogger("PCILeech.ErrorHandler")
        # Ensure the logger has at least one handler
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        # Ensure the error log file exists
        self._ensure_log_file()

    def _ensure_log_file(self):
        """Create the logs directory and error.log file if they do not exist."""
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        self.log_path = os.path.join(log_dir, "error.log")
        if not os.path.exists(self.log_path):
            open(self.log_path, "a").close()

    def handle_error(self, error: Exception, context: str, severity: str = "error") -> None:
        """
        Centralized error handling with context
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
            severity: Error severity level ("error", "warning", "critical")
        """
        # Log the error
        tb_str = "".join(traceback.format_exception(
            type(error), error, error.__traceback__))
        if severity.lower() == "warning":
            self.logger.warning(f"{context}: {error}")
        elif severity.lower() == "critical":
            self.logger.critical(f"{context}: {error}")
        else:
            self.logger.error(f"{context}: {error}")

        # Write traceback to file
        self._write_traceback_to_file(context, tb_str)

        # Get a user‑friendly message
        user_msg = self._get_user_friendly_message(error, context)

        # Notify the user via the app (if possible)
        if hasattr(self.app, "notify_user"):
            self.app.notify_user(user_msg, severity=severity)
        else:
            # Fallback to console output
            print(f"[{severity.upper()}] {user_msg}")

        # If critical, report it
        if severity.lower() == "critical":
            self._report_critical_error(error, context)

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
        context = f"During operation '{operation}'"
        self.handle_error(error, context, severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        """
        Generate a user-friendly error message based on the exception type and context.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        Returns:
            A user-friendly error message
        """
        # Basic mapping for common exception types
        if isinstance(error, FileNotFoundError):
            return f"{context}: Required file not found."
        if isinstance(error, PermissionError):
            return f"{context}: Permission denied."
        if isinstance(error, ValueError):
            return f"{context}: Invalid value provided."
        if isinstance(error, ConnectionError):
            return f"{context}: Network connection failed."
        # Default fallback
        return f"{context}: An unexpected error occurred: {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        """
        Report critical errors for later analysis or immediate attention.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        """
        # For now, just log the critical error. In a real application this could
        # send an email, push to a monitoring service, etc.
        self.logger.critical(f"CRITICAL: {context}: {error}")

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        """
        Append a timestamped traceback to the persistent error log.
        The log is stored under `logs/error.log` relative to the repository root.
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        entry = f"\n=== {timestamp} ===\nContext: {context}\nTraceback:\n{tb_str}\n"
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            # If writing to the log fails, fall back to console
            self.logger.error(f"Failed to write to error log: {e}")
