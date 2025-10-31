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
        self.logger = None
        if hasattr(app, 'logger') and isinstance(getattr(app, 'logger'), logging.Logger):
            self.logger = app.logger
        else:
            self.logger = logging.getLogger('PCILeechTUI.ErrorHandler')

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        '''
        Centralized error handling with context
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        sev = (severity or 'error').lower()
        if sev not in ('warning', 'error', 'critical'):
            sev = 'error'

        friendly_msg = self._get_user_friendly_message(error, context)
        exc_name = type(error).__name__
        log_prefix = f'[{sev.upper()}] {context}: {exc_name}: {error}'
        tb_str = ''.join(traceback.format_exception(
            type(error), error, error.__traceback__))

        if sev == 'warning':
            self.logger.warning(log_prefix)
        elif sev == 'critical':
            self.logger.critical(f'{log_prefix}\n{tb_str}')
        else:
            self.logger.error(f'{log_prefix}\n{tb_str}')

        self._notify_user(friendly_msg, sev)

        if sev == 'critical':
            self._report_critical_error(error, context)

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        '''
        Handle errors that occur during specific operations with a standard format.
        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        context = f'While {operation}'
        self.handle_error(error, context, severity=severity)

    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        '''
        Generate a user-friendly error message based on the exception type and context.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        Returns:
            A user-friendly error message
        '''
        exc = type(error)
        base = f'{context} failed'

        if isinstance(error, FileNotFoundError):
            return f'{base}: File or path not found. Please check the path and try again.'
        if isinstance(error, PermissionError):
            return f'{base}: Permission denied. Try running with elevated privileges or adjust permissions.'
        if isinstance(error, TimeoutError):
            return f'{base}: Operation timed out. Please verify connectivity and try again.'
        if isinstance(error, ConnectionError):
            return f'{base}: Connection error. Ensure the target is reachable and settings are correct.'
        if isinstance(error, OSError):
            return f'{base}: OS error occurred: {error}'
        if isinstance(error, ValueError):
            return f'{base}: Invalid value provided. Please verify the inputs.'
        if isinstance(error, RuntimeError):
            return f'{base}: A runtime error occurred: {error}'
        if isinstance(error, MemoryError):
            return f'{base}: Not enough memory to complete the operation.'
        if isinstance(error, KeyboardInterrupt):
            return f'{base}: Operation was cancelled by user.'
        # Fallback
        return f'{base}: {exc.__name__}: {error}'

    def _report_critical_error(self, error: Exception, context: str) -> None:
        '''
        Report critical errors for later analysis or immediate attention.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        '''
        tb_str = ''.join(traceback.format_exception(
            type(error), error, error.__traceback__))
        self._write_traceback_to_file(context, tb_str)

        log_file = self._get_log_file_path()
        message = f'Critical error recorded. See log file at: {log_file}'
        self._notify_user(message, 'critical')

        report_method = getattr(self.app, 'report_critical_error', None)
        if callable(report_method):
            try:
                report_method(error=error, context=context,
                              traceback_str=tb_str, log_path=str(log_file))
            except Exception as e:
                self.logger.error(
                    f'Failed to call app.report_critical_error: {e}')

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        '''Append a timestamped traceback to the persistent error log.
        The log is stored under `logs/error.log` relative to the repository root.
        '''
        log_file = self._get_log_file_path()
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            header = f'[{timestamp}] Context: {context}\n'
            separator = '-' * 80 + '\n'
            with log_file.open('a', encoding='utf-8') as f:
                f.write(header)
                f.write(tb_str)
                if not tb_str.endswith('\n'):
                    f.write('\n')
                f.write(separator)
        except Exception as e:
            self.logger.error(f'Failed to write traceback to file: {e}')

    def _notify_user(self, message: str, severity: str) -> None:
        notifier = None
        for attr in ('notify', 'notify_user', 'show_message', 'show_error', 'status'):
            cand = getattr(self.app, attr, None)
            if callable(cand):
                notifier = cand
                break

        if notifier:
            try:
                # Try common calling conventions
                try:
                    notifier(message, level=severity)
                except TypeError:
                    notifier(message)
            except Exception as e:
                self.logger.debug(f'User notifier failed: {e}')
        else:
            # Fallback to logger
            if severity == 'warning':
                self.logger.warning(message)
            elif severity == 'critical':
                self.logger.critical(message)
            else:
                self.logger.error(message)

    def _get_log_file_path(self) -> Path:
        repo_root = self._resolve_repo_root()
        return repo_root.joinpath('logs', 'error.log')

    def _resolve_repo_root(self) -> Path:
        module = sys.modules.get(self.__class__.__module__)
        start_path: Optional[Path] = None
        if module is not None:
            module_file = getattr(module, '__file__', None)
            if module_file:
                start_path = Path(module_file).resolve().parent

        if start_path is None:
            start_path = Path.cwd().resolve()

        for parent in [start_path] + list(start_path.parents):
            if parent.joinpath('.git').exists():
                return parent
        return start_path.anchor and Path(start_path.anchor) or start_path.parents[-1] if start_path.parents else start_path
