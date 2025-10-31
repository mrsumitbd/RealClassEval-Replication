import logging
import os
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
        self.logger = None
        try:
            if hasattr(app, "logger") and app.logger:
                self.logger = app.logger
            else:
                self.logger = logging.getLogger("pcileech_tui")
                if not self.logger.handlers:
                    handler = logging.StreamHandler(sys.stderr)
                    formatter = logging.Formatter(
                        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                    )
                    handler.setFormatter(formatter)
                    self.logger.addHandler(handler)
                    self.logger.setLevel(logging.INFO)
        except Exception:
            # Fallback logger in case anything above fails
            self.logger = logging.getLogger("pcileech_tui_fallback")
            if not self.logger.handlers:
                self.logger.addHandler(logging.StreamHandler(sys.stderr))
                self.logger.setLevel(logging.INFO)

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        '''
        Centralized error handling with context
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        try:
            severity = (severity or "error").lower()
            level = self._severity_to_level(severity)
            tb_str = "".join(traceback.format_exception(
                type(error), error, error.__traceback__))
            user_msg = self._get_user_friendly_message(error, context)

            # Log with traceback for developers
            self._log_with_level(
                level, f"{context}: {error.__class__.__name__}: {error}")
            if level >= logging.ERROR:
                self._log_with_level(level, tb_str.strip())

            # Notify the user in the UI (best-effort)
            self._notify_user(user_msg, severity)

            # Persist traceback and report when critical
            if severity == "critical":
                self._write_traceback_to_file(context, tb_str)
                self._report_critical_error(error, context)
        except Exception as handler_exc:
            # Last-resort: ensure the application doesn't crash due to the handler
            try:
                fallback_msg = f"ErrorHandler failure while handling {context}: {handler_exc}"
                self._log_with_level(logging.CRITICAL, fallback_msg)
            except Exception:
                pass

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        '''
        Handle errors that occur during specific operations with a standard format.
        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        context = f"Operation failed while {operation}"
        self.handle_error(error, context, severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        '''
        Generate a user-friendly error message based on the exception type and context.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        Returns:
            A user-friendly error message
        '''
        base = f"{context}: "
        if isinstance(error, FileNotFoundError):
            return f"{base}Required file or path was not found. Please verify the path and try again."
        if isinstance(error, PermissionError):
            return f"{base}Permission denied. Try running with appropriate privileges or adjust permissions."
        if isinstance(error, TimeoutError):
            return f"{base}The operation timed out. Check connectivity or increase the timeout and retry."
        if isinstance(error, ConnectionError):
            return f"{base}A connection error occurred. Verify network/cable and device availability."
        if isinstance(error, ValueError):
            return f"{base}Received an invalid value. Please check your input and try again."
        if isinstance(error, OSError):
            return f"{base}A system error occurred: {error.strerror or 'OS error'}. Please retry."
        if isinstance(error, MemoryError):
            return f"{base}The system is low on memory. Close other applications and try again."
        if isinstance(error, RuntimeError):
            return f"{base}An unexpected runtime error occurred. Please try again."
        if isinstance(error, KeyboardInterrupt):
            return f"{base}Operation was canceled by user."
        # Generic fallback
        return f"{base}An unexpected error occurred: {error}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        '''
        Report critical errors for later analysis or immediate attention.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        '''
        try:
            # Attempt to surface a prominent user notification
            self._notify_user(
                f"Critical error: {context}. Check logs for details.", "critical")

            # If app provides an explicit reporting hook, attempt to use it
            hook = self._get_attr_any(
                self.app, ["report_critical_error", "report_error", "send_telemetry"])
            if callable(hook):
                try:
                    hook({"type": "critical_error",
                         "context": context, "error": repr(error)})
                except Exception:
                    pass
        except Exception:
            pass

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        '''Append a timestamped traceback to the persistent error log.
        The log is stored under `logs/error.log` relative to the repository root.
        '''
        try:
            repo_root = self._find_repo_root() or Path.cwd()
            logs_dir = repo_root / "logs"
            logs_dir.mkdir(parents=True, exist_ok=True)
            log_file = logs_dir / "error.log"

            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            header = f"[{timestamp}] {context}\n"
            separator = "-" * 80 + "\n"

            with log_file.open("a", encoding="utf-8") as f:
                f.write(header)
                f.write(tb_str)
                if not tb_str.endswith("\n"):
                    f.write("\n")
                f.write(separator)
        except Exception:
            try:
                self._log_with_level(
                    logging.ERROR, "Failed to write traceback to file.")
            except Exception:
                pass

    # ----------------------- Helper methods -----------------------

    def _notify_user(self, message: str, severity: str) -> None:
        try:
            severity = (severity or "error").lower()
            # Preferred: app.notify(message, level=severity)
            notify = getattr(self.app, "notify", None)
            if callable(notify):
                try:
                    notify(message, level=severity)
                    return
                except TypeError:
                    notify(message)  # Fallback signature
                    return

            # Alternative common names
            alt = self._get_attr_any(
                self.app, ["show_notification", "show_message", "toast", "status"])
            if callable(alt):
                try:
                    alt(message)
                    return
                except Exception:
                    pass

            # UI container patterns (e.g., app.ui.error)
            ui = getattr(self.app, "ui", None)
            if ui is not None:
                ui_method = self._get_attr_any(
                    ui, ["error", "warning", "info", "notify", "message"])
                if callable(ui_method):
                    try:
                        ui_method(message)
                        return
                    except Exception:
                        pass

            # Last resort
            print(message, file=sys.stderr)
        except Exception:
            pass

    def _severity_to_level(self, severity: str) -> int:
        mapping = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }
        return mapping.get(severity.lower(), logging.ERROR)

    def _log_with_level(self, level: int, msg: str) -> None:
        try:
            if level >= logging.CRITICAL:
                self.logger.critical(msg)
            elif level >= logging.ERROR:
                self.logger.error(msg)
            elif level >= logging.WARNING:
                self.logger.warning(msg)
            elif level >= logging.INFO:
                self.logger.info(msg)
            else:
                self.logger.debug(msg)
        except Exception:
            # As a fallback, write to stderr
            try:
                print(msg, file=sys.stderr)
            except Exception:
                pass

    def _find_repo_root(self) -> Optional[Path]:
        candidates = [".git", "pyproject.toml",
                      "setup.cfg", "setup.py", "requirements.txt"]
        try:
            start = Path(__file__).resolve().parent
        except Exception:
            start = Path.cwd()

        for path in [start, *start.parents]:
            try:
                if any((path / c).exists() for c in candidates):
                    return path
            except Exception:
                continue
        return None

    @staticmethod
    def _get_attr_any(obj, names):
        for n in names:
            if hasattr(obj, n):
                return getattr(obj, n)
        return None
