
import os
import logging
import traceback
from datetime import datetime
from typing import Optional


class ErrorHandler:
    """
    Centralized error handling system for the PCILeech TUI application.
    This class provides a consistent way to handle errors throughout the
    application, including logging, user notifications, and critical error
    reporting.
    """

    def __init__(self, app):
        """
        Initialize the error handler with the app instance.

        Args:
            app: The main TUI application instance
        """
        self.app = app
        # Prefer an existing logger from the app, otherwise create one
        self.logger: logging.Logger = getattr(
            app, "logger", logging.getLogger("ErrorHandler"))
        if not self.logger.handlers:
            # Basic configuration if no handlers are present
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.DEBUG)

        # Ensure the error log directory exists
        self.log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, "error.log")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def handle_error(self, error: Exception, context: str, severity: str = "error") -> None:
        """
        Centralized error handling with context.

        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
            severity: Error severity level ("error", "warning", "critical")
        """
        # Log the error
        if severity == "critical":
            self.logger.critical(f"{context}: {error}")
        elif severity == "warning":
            self.logger.warning(f"{context}: {error}")
        else:
            self.logger.error(f"{context}: {error}")

        # Get a user‑friendly message
        user_msg = self._get_user_friendly_message(error, context)

        # Notify the user via the app if possible
        notify_method = getattr(self.app, "notify_user", None)
        if callable(notify_method):
            notify_method(user_msg, severity=severity)
        else:
            # Fallback to console output
            print(f"[{severity.upper()}] {user_msg}")

        # If critical, report it
        if severity == "critical":
            self._report_critical_error(error, context)

        # Write traceback to file
        tb_str = "".join(traceback.format_exception(
            type(error), error, error.__traceback__))
        self._write_traceback_to_file(context, tb_str)

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
        context = f"Error during {operation}"
        self.handle_error(error, context, severity)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
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
            return f"File not found while {context}. Please verify the path."
        if isinstance(error, PermissionError):
            return f"Permission denied while {context}. Check your access rights."
        if isinstance(error, ConnectionError):
            return f"Network error while {context}. Ensure you are connected."
        if isinstance(error, ValueError):
            return f"Invalid value encountered during {context}. {error}"
        if isinstance(error, RuntimeError):
            return f"Runtime error during {context}. {error}"
        # Default fallback
        return f"An error occurred while {context}: {error}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        """
        Report critical errors for later analysis or immediate attention.

        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        """
        # For now, just log the critical error. In a real system this could
        # send an email, push to a monitoring service, etc.
        self.logger.critical(f"CRITICAL: {context}: {error}")

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        """
        Append a timestamped traceback to the persistent error log.
        The log is stored under `logs/error.log` relative to the repository root.
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        entry = (
            f"\n=== {timestamp} ===\n"
            f"Context: {context}\n"
            f"Traceback:\n{tb_str}\n"
            f"=== End of entry ===\n"
        )
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            # If writing to the log fails, fall back to console
            self.logger.error(f"Failed to write error log: {e}")
