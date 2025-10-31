import logging
import os
import sys
import traceback
from datetime import datetime


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
        self.logger = getattr(app, 'logger', logging.getLogger('pcileech.tui'))
        if not self.logger.handlers:
            # Avoid duplicate handlers if app provided one; set a sane default.
            handler = logging.StreamHandler(sys.stderr)
            formatter = logging.Formatter(
                '%(asctime)s %(levelname)s %(name)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        self.repo_root = getattr(
            app, 'repo_root', None) or self._find_repo_root()
        self.log_dir = os.path.join(self.repo_root, 'logs')
        self.error_log_path = os.path.join(self.log_dir, 'error.log')

    def handle_error(self, error: Exception, context: str, severity: str = 'error') -> None:
        '''
        Centralized error handling with context
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        sev = (severity or 'error').lower()
        if sev not in ('error', 'warning', 'critical'):
            sev = 'error'

        msg = self._get_user_friendly_message(error, context)
        tb_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__)) if getattr(
            error, '__traceback__', None) else str(error)

        # Log with appropriate level
        if sev == 'warning':
            self.logger.warning('%s: %s', context, repr(error))
        elif sev == 'critical':
            self.logger.critical('%s: %s', context, repr(error))
        else:
            self.logger.error('%s: %s', context, repr(error))

        # Write full traceback to persistent log
        try:
            self._write_traceback_to_file(context, tb_str)
        except Exception as log_err:
            # Fallback log if writing fails
            self.logger.error(
                'Failed to write error traceback to file: %r', log_err)

        # Notify user via app if possible
        self._notify_user(msg, sev)

        # Report critical errors
        if sev == 'critical':
            try:
                self._report_critical_error(error, context)
            except Exception as report_err:
                self.logger.error(
                    'Failed to report critical error: %r', report_err)

    def handle_operation_error(self, operation: str, error: Exception, severity: str = 'error') -> None:
        '''
        Handle errors that occur during specific operations with a standard format.
        Args:
            operation: The operation that failed (e.g., "scanning devices", "starting build")
            error: The exception that occurred
            severity: Error severity level ("error", "warning", "critical")
        '''
        operation = operation.strip() if isinstance(operation, str) else str(operation)
        context = f'Operation "{operation}" failed'
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
        etype = type(error).__name__
        base = str(error).strip()

        if isinstance(error, FileNotFoundError):
            return f'{context}: Required file or path was not found. {base}'
        if isinstance(error, PermissionError):
            return f'{context}: Permission denied. Please check access rights. {base}'
        if isinstance(error, TimeoutError):
            return f'{context}: The operation timed out. Consider retrying or checking connectivity.'
        if isinstance(error, ConnectionError) or etype in ('ConnectionRefusedError', 'ConnectionResetError', 'ConnectionAbortedError'):
            return f'{context}: A connection error occurred. Please verify device or network connectivity. {base}'
        if isinstance(error, ValueError):
            return f'{context}: Invalid value encountered. {base}'
        if isinstance(error, OSError):
            return f'{context}: A system error occurred. {base}'
        if isinstance(error, RuntimeError):
            return f'{context}: Runtime error. {base}'
        # Default
        return f'{context}: {etype}: {base or "An unexpected error occurred."}'

    def _report_critical_error(self, error: Exception, context: str) -> None:
        '''
        Report critical errors for later analysis or immediate attention.
        Args:
            error: The exception that occurred
            context: Description of where/when the error occurred
        '''
        # Hook for integrations (telemetry, sentry, etc.) if present on app
        reporter = getattr(self.app, 'report_critical', None)
        if callable(reporter):
            try:
                reporter(error=error, context=context,
                         log_path=self.error_log_path)
            except Exception as e:
                self.logger.error('Critical reporter failed: %r', e)

        # Ensure user is explicitly made aware for critical issues
        self._notify_user(
            f'Critical error in {context}. Details have been written to {self.error_log_path}.',
            'critical'
        )

    def _write_traceback_to_file(self, context: str, tb_str: str) -> None:
        '''Append a timestamped traceback to the persistent error log.
        The log is stored under `logs/error.log` relative to the repository root.
        '''
        os.makedirs(self.log_dir, exist_ok=True)
        timestamp = datetime.utcnow().isoformat(timespec='seconds') + 'Z'
        header = f'[{timestamp}] Context: {context}'
        content = f'{header}\n{tb_str}\n{"-"*72}\n'
        with open(self.error_log_path, 'a', encoding='utf-8') as f:
            f.write(content)

    def _notify_user(self, message: str, severity: str) -> None:
        notify = getattr(self.app, 'notify', None)
        if callable(notify):
            try:
                notify(message, level=severity)
                return
            except Exception:
                pass
        show_error = getattr(self.app, 'show_error', None)
        if callable(show_error) and severity in ('error', 'critical'):
            try:
                show_error(message)
                return
            except Exception:
                pass
        show_message = getattr(self.app, 'show_message', None)
        if callable(show_message):
            try:
                show_message(message)
                return
            except Exception:
                pass
        print(message, file=sys.stderr)

    def _find_repo_root(self) -> str:
        # Try to locate a project root by walking up for markers
        start = os.getcwd()
        current = os.path.abspath(start)
        markers = ('.git', '.hg', 'pyproject.toml', 'setup.cfg', 'setup.py')
        while True:
            if any(os.path.exists(os.path.join(current, m)) for m in markers):
                return current
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent
        return start
