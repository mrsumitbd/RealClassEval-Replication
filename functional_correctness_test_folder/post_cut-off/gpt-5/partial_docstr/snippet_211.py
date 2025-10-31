import logging
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional


class ErrorHandler:
    '''
    Centralized error handling system for the PCILeech TUI application.
    This class provides a consistent way to handle errors throughout the application,
    including logging, user notifications, and critical error reporting.
    '''

    def __init__(self, app):
        '''
        Initialize the error handler with the app instance.
        Args:
            app: The main TUI application instance
        '''
        self.app = app
        self.logger = logging.getLogger("pcileech_tui")
        # Ensure logger has at least a NullHandler to avoid "No handlers could be found"
        if not self.logger.handlers:
            self.logger.addHandler(logging.NullHandler())
        self.logger.setLevel(logging.INFO)

        # Default error logs directory: ~/.pcileech_tui/logs
        self._logs_dir = Path.home() / ".pcileech_tui" / "logs"
        try:
            self._logs_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            # Fallback to current working directory if home is not writable
            self._logs_dir = Path.cwd() / "pcileech_tui_logs"
            self._logs_dir.mkdir(parents=True, exist_ok=True)

        self._last_report_path: Optional[Path] = None

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        level = self._map_severity_to_level(severity)
        friendly = self._get_user_friendly_message(error, context)

        tb_str = "".join(traceback.format_exception(
            type(error), error, error.__traceback__))

        # Log with traceback
        self.logger.log(level, f"{context}: {error}", exc_info=error)

        if severity.lower() == "critical":
            self._report_critical_error(error, context)
        else:
            # For non-critical, optionally write traceback to file for later reference
            try:
                self._write_traceback_to_file(context, tb_str)
                hint = f" Details have been saved to: {self._last_report_path}" if self._last_report_path else ""
            except Exception:
                hint = ""
            self._notify_user(friendly + hint, severity)

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        '''
        Handle errors that occur during specific operations with a standard format.
        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        context = f"Error during {operation}"
        self.handle_error(error, context, severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        if isinstance(error, FileNotFoundError):
            return f"{context}: Required file or path was not found."
        if isinstance(error, PermissionError):
            return f"{context}: Permission denied. Please check your access rights."
        if isinstance(error, TimeoutError):
            return f"{context}: Operation timed out. Try again or check connectivity."
        if isinstance(error, ConnectionError):
            return f"{context}: Unable to establish a connection. Verify network/cable/device."
        if isinstance(error, ValueError):
            return f"{context}: Invalid value provided. {str(error) or 'Please verify input.'}"
        if isinstance(error, OSError):
            return f"{context}: System I/O error occurred. {str(error) or ''}".rstrip()
        # Fallback generic message
        details = str(error).strip()
        return f"{context}: {details or type(error).__name__}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        tb_str = "".join(traceback.format_exception(
            type(error), error, error.__traceback__))
        try:
            self._write_traceback_to_file(context, tb_str)
        except Exception:
            self._last_report_path = None

        path_msg = f"\nA detailed error report was saved to: {self._last_report_path}" if self._last_report_path else ""
        msg = (
            f"Critical error: {self._get_user_friendly_message(error, context)}{path_msg}\n"
            "The application may be unstable. Consider restarting."
        )
        self.logger.critical(f"{context}: {error}", exc_info=error)
        self._notify_user(msg, "critical")

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_ctx = "".join(ch if ch.isalnum() or ch in (
            "-", "_") else "_" for ch in context).strip("_")
        safe_ctx = (safe_ctx[:50] + "...") if len(safe_ctx) > 60 else safe_ctx
        filename = f"error_{timestamp}_{safe_ctx or 'context'}.log"
        path = self._logs_dir / filename

        header = [
            f"Timestamp: {datetime.now().isoformat()}",
            f"Context: {context}",
            "-" * 80,
            tb_str,
        ]
        data = "\n".join(header)

        path.write_text(data, encoding="utf-8")
        self._last_report_path = path

    def _map_severity_to_level(self, severity: str) -> int:
        sev = (severity or "error").lower()
        if sev == "warning":
            return logging.WARNING
        if sev == "critical":
            return logging.CRITICAL
        return logging.ERROR

    def _notify_user(self, message: str, severity: str = "error") -> None:
        sev = (severity or "error").lower()
        # Try several common app notification hooks safely
        try:
            if hasattr(self.app, "notify") and callable(getattr(self.app, "notify")):
                self.app.notify(message, severity=sev)
                return
            if hasattr(self.app, "show_notification") and callable(getattr(self.app, "show_notification")):
                self.app.show_notification(message, severity=sev)
                return
            if hasattr(self.app, "show_error") and callable(getattr(self.app, "show_error")) and sev in ("error", "critical"):
                self.app.show_error(message)
                return
            if hasattr(self.app, "show_message") and callable(getattr(self.app, "show_message")):
                self.app.show_message(message)
                return
            if hasattr(self.app, "print") and callable(getattr(self.app, "print")):
                self.app.print(message)
                return
        except Exception:
            pass
        stream = sys.stderr if sev in ("error", "critical") else sys.stdout
        try:
            print(message, file=stream)
        except Exception:
            pass
