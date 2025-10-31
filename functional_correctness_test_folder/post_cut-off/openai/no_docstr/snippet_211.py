
import logging
import os
import traceback
from datetime import datetime
from typing import Optional


class ErrorHandler:
    """
    A simple error handling utility that logs errors, generates user‑friendly messages,
    and writes tracebacks for critical errors to a file.
    """

    def __init__(self, app: Optional[object] = None):
        """
        Initialize the error handler.

        Parameters
        ----------
        app : object, optional
            The application instance (e.g., Flask, Django). It is not used directly
            but can be stored for future extensions.
        """
        self.app = app
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            # Basic configuration if no handlers are present
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        # Directory to store traceback files
        self.traceback_dir = os.path.join(os.getcwd(), "error_tracebacks")
        os.makedirs(self.traceback_dir, exist_ok=True)

    def handle_error(self, error: Exception, context: str, severity: str = "error") -> None:
        """
        Handle a generic error: log it, generate a user‑friendly message, and
        report critical errors.

        Parameters
        ----------
        error : Exception
            The exception instance.
        context : str
            A description of where the error occurred.
        severity : str, optional
            One of 'debug', 'info', 'warning', 'error', 'critical'.
        """
        user_msg = self._get_user_friendly_message(error, context)
        log_msg = f"[{context}] {user_msg} | Exception: {repr(error)}"

        # Log according to severity
        if severity.lower() == "debug":
            self.logger.debug(log_msg)
        elif severity.lower() == "info":
            self.logger.info(log_msg)
        elif severity.lower() == "warning":
            self.logger.warning(log_msg)
        elif severity.lower() == "critical":
            self.logger.critical(log_msg)
            self._report_critical_error(error, context)
        else:  # default to error
            self.logger.error(log_msg)

    def handle_operation_error(self, operation: str, error: Exception, severity: str = "error") -> None:
        """
        Handle an error that occurred during a specific operation.

        Parameters
        ----------
        operation : str
            Name or description of the operation.
        error : Exception
            The exception instance.
        severity : str, optional
            One of 'debug', 'info', 'warning', 'error', 'critical'.
        """
        context = f"Operation '{operation}'"
        self.handle_error(error, context, severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        """
        Return a user‑friendly message based on the exception type.

        Parameters
        ----------
        error : Exception
            The exception instance.
        context : str
            Context string for debugging purposes.

        Returns
        -------
        str
            A message suitable for end users.
        """
        if isinstance(error, ValueError):
            return "Invalid input provided."
        if isinstance(error, KeyError):
            return "A required field is missing."
        if isinstance(error, FileNotFoundError):
            return "The requested file could not be found."
        if isinstance(error, PermissionError):
            return "You do not have permission to perform this action."
        # Default generic message
        return "An unexpected error occurred. Please try again later."

    def _report_critical_error(self, error: Exception, context: str) -> None:
        """
        For critical errors, write the full traceback to a file.

        Parameters
        ----------
        error : Exception
            The exception instance.
        context : str
            Context string for debugging purposes.
        """
        tb_str = "".join(traceback.format_exception(
            type(error), error, error.__traceback__))
        self._write_traceback_to_file(context, tb_str)

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        """
        Write the traceback string to a timestamped file.

        Parameters
        ----------
        context : str
            Context string for naming the file.
        tb_str : str
            The traceback string to write.
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        safe_context = "".join(c if c.isalnum() or c in (
            "_", "-") else "_" for c in context)
        filename = f"{timestamp}_{safe_context}.log"
        filepath = os.path.join(self.traceback_dir, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(tb_str)
            self.logger.info(f"Critical error traceback written to {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to write traceback to file: {e}")
