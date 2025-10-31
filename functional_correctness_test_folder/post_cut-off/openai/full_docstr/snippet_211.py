
import os
import sys
import traceback
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional


class ErrorHandler:
    """
    Centralized error handling system for the PCILeech TUI application.
    This class provides a consistent way to handle errors throughout the application,
    including logging, user notifications, and critical error reporting.
    """

    LOG_DIR = Path("logs")
    LOG_FILE = LOG_DIR / "error.log"

    def __init__(self, app):
        """
        Initialize the error handler with the app instance.
        Args:
            app: The main TUI application instance
        """
        self.app = app
        self.logger = logging.getLogger("ErrorHandler")
        self.logger.setLevel(logging.DEBUG)

        # Ensure log directory exists
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)

        # File handler for persistent logging
        fh = logging.FileHandler(self.LOG_FILE, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        # Console handler for immediate feedback
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def handle_error(self, error: Exception, context: str, severity: str = "error") -> None:
        """
        Centralized error handling with context
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
            severity: Error severity level ("error", "warning", "critical")
        """
        tb_str = "".join(traceback.format_exception(
            type(error), error, error.__traceback__))
        self._write_traceback_to_file(context, tb_str)

        user_msg = self._get_user_friendly_message(error, context)

        # Log according to severity
        if severity == "critical":
            self.logger.critical(f"{context}: {user_msg}\n{tb_str}")
            self._report_critical_error(error, context)
        elif severity == "warning":
            self.logger.warning(f"{context}: {user_msg}\n{tb_str}")
        else:
            self.logger.error(f"{context}: {user_msg}\n{tb_str}")

        # Notify user via app if possible
        if hasattr(self.app, "notify"):
            try:
                self.app.notify(user_msg, severity=severity)
            except Exception:
                # Fallback to simple print
                print(f"[{severity.upper()}] {user_msg}")
        else:
            print(f"[{severity.upper()}] {user_msg}")

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
        if isinstance(error, FileNotFoundError):
            return f"File not found while {context}. Please check the path."
        if isinstance(error, PermissionError):
            return f"Permission denied while {context}. Try running with elevated privileges."
        if isinstance(error, ValueError):
            return f"Invalid value encountered during {context}. Verify your input."
        if isinstance(error, ConnectionError):
            return f"Network error during {context}. Check your connection."
        if isinstance(error, TimeoutError):
            return f"Operation timed out during {context}. Try again later."
        # Default generic message
        return f"An error occurred during {context}. See logs for details."

    def _report_critical_error(self, error: Exception, context: str) -> None:
        """
        Report critical errors for later analysis or immediate attention.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        """
        # In a real application, this could send an email, trigger an alert, etc.
        # For now, we simply log a special message.
        self.logger.critical(f"CRITICAL: {context} - {error}")

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        """
        Append a timestamped traceback to the persistent error log.
        The log is stored under `logs/error.log` relative to the repository root.
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        entry = f"\n=== {timestamp} ===\nContext: {context}\nTraceback:\n{tb_str}\n"
        try:
            with open(self.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception:
            # If writing to file fails, fall back to console
            print(f"Failed to write error log: {entry}")
