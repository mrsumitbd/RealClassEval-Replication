import logging
import os
import sys
import tempfile
import traceback
from datetime import datetime
from typing import Optional


class ErrorHandler:
    def __init__(self, app):
        self.app = app
        self.logger = getattr(app, "logger", None)
        if self.logger is None:
            name = getattr(app, "__class__", type("App", (), {})).__name__
            self.logger = logging.getLogger(f"{__name__}.{name}")
            if not self.logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        self.log_dir = (
            getattr(app, "log_dir", None)
            or getattr(app, "logs_dir", None)
            or os.path.join(os.getcwd(), "logs")
        )
        try:
            os.makedirs(self.log_dir, exist_ok=True)
        except Exception:
            # Fallback to temp dir if unable to create
            self.log_dir = tempfile.gettempdir()

    def handle_error(self, error: Exception, context: str, severity: str = "error") -> None:
        severity = (severity or "error").lower()
        if severity not in ("debug", "info", "warning", "error", "critical"):
            severity = "error"

        friendly_message = self._get_user_friendly_message(error, context)
        tb_str = "".join(traceback.format_exception(
            type(error), error, error.__traceback__))

        log_msg = f"{context} - {friendly_message}"
        if severity == "debug":
            self.logger.debug(log_msg)
        elif severity == "info":
            self.logger.info(log_msg)
        elif severity == "warning":
            self.logger.warning(log_msg)
        elif severity == "critical":
            self.logger.critical(log_msg)
        else:
            self.logger.error(log_msg)

        if severity in ("error", "critical"):
            self._write_traceback_to_file(context, tb_str)

        notifier = getattr(self.app, "notify", None) or getattr(
            self.app, "show_message", None)
        if callable(notifier):
            try:
                notifier(friendly_message, level=severity)
            except TypeError:
                try:
                    notifier(friendly_message)
                except Exception:
                    pass

        if severity == "critical":
            self._report_critical_error(error, context)

    def handle_operation_error(self, operation: str, error: Exception, severity: str = "error") -> None:
        op = operation or "operation"
        context = f"While performing '{op}'"
        self.handle_error(error, context, severity=severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        base = str(error).strip() or error.__class__.__name__
        if isinstance(error, FileNotFoundError):
            return f"{context}: The required file or resource was not found."
        if isinstance(error, PermissionError):
            return f"{context}: Permission denied. Please check your access rights."
        if isinstance(error, TimeoutError):
            return f"{context}: The operation timed out. Please try again."
        if isinstance(error, ConnectionError):
            return f"{context}: A connection error occurred. Please check your network."
        if isinstance(error, ValueError):
            return f"{context}: Received an invalid value. {base}"
        if isinstance(error, KeyError):
            missing = base.strip("'\"")
            return f"{context}: Missing required key: {missing}"
        if isinstance(error, IndexError):
            return f"{context}: An item was accessed out of range."
        if isinstance(error, ZeroDivisionError):
            return f"{context}: Division by zero is not allowed."
        if isinstance(error, MemoryError):
            return f"{context}: The application ran out of memory."
        if isinstance(error, OSError):
            return f"{context}: A system error occurred. {base}"
        return f"{context}: {base}"

    def _report_critical_error(self, error: Exception, context: str) -> None:
        tb_str = "".join(traceback.format_exception(
            type(error), error, error.__traceback__))
        self.logger.critical(f"Critical error in {context}: {error}")
        self._write_traceback_to_file(f"CRITICAL - {context}", tb_str)

        reporter = (
            getattr(self.app, "report_critical", None)
            or getattr(self.app, "on_critical_error", None)
        )
        if callable(reporter):
            try:
                reporter(error=error, context=context, traceback_str=tb_str)
                return
            except TypeError:
                try:
                    reporter(error, context, tb_str)  # positional fallback
                except Exception:
                    pass
            except Exception:
                pass

        notifier = getattr(self.app, "notify", None) or getattr(
            self.app, "show_message", None)
        if callable(notifier):
            try:
                notifier(
                    f"A critical error occurred in {context}. Please check logs.", level="critical")
            except TypeError:
                try:
                    notifier(
                        f"A critical error occurred in {context}. Please check logs.")
                except Exception:
                    pass

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        safe_context = "".join(c if c.isalnum() or c in (
            "-", "_") else "_" for c in (context or "context"))
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = f"traceback_{timestamp}_{safe_context[:40]}.log"
        path = os.path.join(self.log_dir, filename)
        header = [
            f"Timestamp: {datetime.utcnow().isoformat()}Z",
            f"Context: {context}",
            f"Python: {sys.version.split()[0]}",
            f"Platform: {sys.platform}",
            "-" * 80,
        ]
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(header))
                f.write("\n")
                f.write(tb_str if tb_str.endswith("\n") else tb_str + "\n")
        except Exception:
            # As a last resort, try writing to temp dir
            try:
                fallback_path = os.path.join(tempfile.gettempdir(), filename)
                with open(fallback_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(header))
                    f.write("\n")
                    f.write(tb_str if tb_str.endswith("\n") else tb_str + "\n")
            except Exception:
                pass
