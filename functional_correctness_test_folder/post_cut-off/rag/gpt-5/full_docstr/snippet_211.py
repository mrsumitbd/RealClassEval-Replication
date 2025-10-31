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
        self.logger = getattr(app, 'logger', None)
        if self.logger is None:
            self.logger = logging.getLogger('pcileech_tui')
            if not self.logger.handlers:
                self.logger.setLevel(logging.INFO)
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(asctime)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
        self.last_error: Optional[dict] = None

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        '''
        Centralized error handling with context
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        user_msg = self._get_user_friendly_message(error, context)
        tb_str = ''.join(traceback.format_exception(
            type(error), error, error.__traceback__))

        sev = (severity or 'error').lower()
        if sev == 'critical':
            self.logger.critical(f'{context}: {error}', exc_info=error)
        elif sev == 'warning':
            self.logger.warning(f'{context}: {error}')
            self.logger.debug(tb_str)
        else:
            self.logger.error(f'{context}: {error}', exc_info=error)

        notified = False
        try:
            if hasattr(self.app, 'notify') and callable(self.app.notify):
                try:
                    self.app.notify(user_msg, level=sev)
                except TypeError:
                    self.app.notify(user_msg)
                notified = True
            elif sev == 'warning' and hasattr(self.app, 'show_warning') and callable(self.app.show_warning):
                self.app.show_warning(user_msg)
                notified = True
            elif sev in ('error', 'critical') and hasattr(self.app, 'show_error') and callable(self.app.show_error):
                self.app.show_error(user_msg)
                notified = True
            elif hasattr(self.app, 'status') and callable(self.app.status):
                self.app.status(user_msg)
                notified = True
        except Exception:
            pass

        if not notified:
            try:
                print(user_msg, file=sys.stderr)
            except Exception:
                pass

        if sev == 'critical':
            self._report_critical_error(error, context)

        self.last_error = {
            'error': error,
            'context': context,
            'severity': sev,
            'traceback': tb_str,
            'message': user_msg
        }

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        '''
        Handle errors that occur during specific operations with a standard format.
        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        context = f'Error during {operation}'
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
        base = str(error).strip() or error.__class__.__name__
        if isinstance(error, FileNotFoundError):
            msg = 'Required file or path not found'
        elif isinstance(error, PermissionError):
            msg = 'Permission denied'
        elif isinstance(error, TimeoutError):
            msg = 'Operation timed out'
        elif isinstance(error, ConnectionError):
            msg = 'Connection failed'
        elif isinstance(error, ValueError):
            msg = 'Invalid value encountered'
        elif isinstance(error, OSError):
            msg = 'System I/O error'
        elif isinstance(error, RuntimeError):
            msg = 'Runtime error'
        else:
            msg = 'Unexpected error'
        details = f' ({base})' if base and base.lower(
        ) not in msg.lower() else ''
        return f'{context}: {msg}{details}'

    def _report_critical_error(self, error: Exception, context: str) -> None:
        '''
        Report critical errors for later analysis or immediate attention.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        '''
        tb_str = ''.join(traceback.format_exception(
            type(error), error, error.__traceback__))
        try:
            self._write_traceback_to_file(context, tb_str)
        except Exception as log_exc:
            self.logger.error(f'Failed to write critical error log: {log_exc}')
        reporter = getattr(self.app, 'report_critical_error', None)
        if callable(reporter):
            try:
                reporter(error=error, context=context, traceback_str=tb_str)
            except Exception as rep_exc:
                self.logger.error(
                    f'Failed to report critical error via app hook: {rep_exc}')

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        '''Append a timestamped traceback to the persistent error log.
        The log is stored under `logs/error.log` relative to the repository root.
        '''
        root = None
        try:
            candidate = getattr(self.app, 'repo_root', None) or getattr(
                self.app, 'root_path', None)
            if candidate:
                root = Path(candidate)
            if root is None:
                cwd = Path.cwd()
                for p in [cwd] + list(cwd.parents):
                    if (p / '.git').exists():
                        root = p
                        break
            if root is None:
                root = Path.cwd()
            logs_dir = root / 'logs'
            logs_dir.mkdir(parents=True, exist_ok=True)
            log_path = logs_dir / 'error.log'
            timestamp = datetime.now().isoformat(timespec='seconds')
            with log_path.open('a', encoding='utf-8') as f:
                f.write(f'[{timestamp}] {context}\n')
                f.write(tb_str.rstrip() + '\n')
                f.write('-' * 80 + '\n')
        except Exception as exc:
            self.logger.error(f'Unable to persist error log: {exc}')
