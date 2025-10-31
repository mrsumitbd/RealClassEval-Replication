
import os
import logging
import traceback
from datetime import datetime
from typing import Any, Optional

# Configure a module‑level logger
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)
# File handler for the error log
_file_handler = logging.FileHandler("logs/error.log")
_file_handler.setLevel(logging.DEBUG)
_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
_file_handler.setFormatter(_formatter)
_logger.addHandler(_file_handler)


class ErrorHandler:
    """
    Centralized error handling system for the PCILeech TUI application.
    This class provides a consistent way to handle errors throughout the application,
    including logging, user notifications, and critical error reporting.
    """

    def __init__(self, app: Any) -> None:
        """
        Initialize the error handler with the app instance.
        Args:
            app: The main TUI application instance
        """
        self.app = app
        # If the app has its own logger, use it; otherwise use the module logger
        self.logger = getattr(app, "logger", _logger)

    def handle_error(
        self,
        error: Exception,
        context: str,
        severity: str = "error",
    ) -> None:
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
        self._write_traceback_to_file(context, tb_str)

        # Determine the log level
        level = {
            "critical": logging.CRITICAL,
            "error": logging.ERROR,
            "warning": logging.WARNING,
        }.get(severity.lower(), logging.ERROR)

        self.logger.log(level, f"{context}: {error}")

        # Generate a user‑friendly message
        user_msg = self._get_user_friendly_message(error, context)

        # Notify the user via the app if possible
        notify = getattr(self.app, "notify", None)
        if callable(notify):
            notify(user_msg, level=severity)
        else:
            # Fallback to console output
            print(f"[{severity.upper()}] {user_msg}")

        # If critical, report it for further analysis
        if severity.lower() == "critical":
            self._report_critical_error(error, context)

    def handle_operation_error(
        self,
        operation: str,
        error: Exception,
        severity: str = "error",
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
        # Specific handling for common exception types
        if isinstance(error, FileNotFoundError):
            return f"File not found while {context}. Please verify the file path."
        if isinstance(error, PermissionError):
            return f"Permission denied while {context}. Check your access rights."
        if isinstance(error, ConnectionError):
            return f"Network error while {context}. Ensure you are connected to the internet."
        if isinstance(error, ValueError):
            return f"Invalid value encountered while {context}. Please check your input."
        # Default fallback
        return f"An error occurred while {context}: {str(error)}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        """
        Report critical errors for later analysis or immediate attention.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        """
        # For now, we simply log the critical error to a dedicated file.
        critical_log_path = os.path.join("logs", "critical_errors.log")
        os.makedirs("logs", exist_ok=True)
        with open(critical_log_path, "a", encoding="utf-8") as f:
            f.write(
                f"{datetime.now().isoformat()} [CRITICAL] {context}: {error}\n"
            )
        # If the app has a method to trigger an alert, call it
        alert = getattr(self.app, "alert", None)
        if callable(alert):
            alert(f"Critical error: {error}")

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        """
        Append a timestamped traceback to the persistent error log.
        The log is stored under `logs/error.log` relative to the repository root.
        """
        # The file handler already writes the timestamp; we just append the context and traceback
        with open("logs/error.log", "a", encoding="utf-8") as f:
            f.write(f"\n--- Context: {context} ---\n")
            f.write(tb_str)
            f.write("\n--- End of traceback ---\n")
