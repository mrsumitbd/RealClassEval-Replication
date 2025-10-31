import logging
import os
import importlib
from typing import Optional, Union, List, Callable, Any


class WebProcessMixin:
    '''
    Mixin class for BedrockServerManager that handles direct Web UI process management.
        '''

    def start_web_ui_direct(self, app_context: 'AppContext', host: Optional[Union[str, List[str]]] = None, debug: bool = False, threads: Optional[int] = None) -> None:
        '''Starts the Web UI application directly in the current process (blocking).
        This method is intended for scenarios where the Web UI is launched with
        the ``--mode direct`` command-line argument. It dynamically imports and
        calls the :func:`~.web.app.run_web_server` function, which in turn
        starts the Uvicorn server hosting the FastAPI application.
        .. note::
            This is a blocking call and will occupy the current process until the
            web server is shut down.
        Args:
            host (Optional[Union[str, List[str]]]): The host address or list of
                addresses for the web server to bind to. Passed directly to
                :func:`~.web.app.run_web_server`. Defaults to ``None``.
            debug (bool): If ``True``, runs the underlying Uvicorn/FastAPI app
                in debug mode (e.g., with auto-reload). Passed directly to
                :func:`~.web.app.run_web_server`. Defaults to ``False``.
            threads (Optional[int]): Specifies the number of worker processes for Uvicorn
                Only used for Windows Service
        Raises:
            RuntimeError: If :func:`~.web.app.run_web_server` raises a RuntimeError
                (e.g., missing authentication environment variables).
            ImportError: If the web application components (e.g.,
                :func:`~.web.app.run_web_server`) cannot be imported.
            Exception: Re-raises other exceptions from :func:`~.web.app.run_web_server`
                if Uvicorn fails to start.
        '''
        logger = getattr(self, '_logger', None) or logging.getLogger(__name__)

        def _candidate_modules() -> List[str]:
            mods: List[str] = []
            sources = [self.__class__.__module__]
            if app_context is not None:
                sources.append(type(app_context).__module__)
            for src in sources:
                if not src:
                    continue
                parts = src.split('.')
                for i in range(len(parts), 0, -1):
                    base = '.'.join(parts[:i])
                    candidate = f'{base}.web.app'
                    if candidate not in mods:
                        mods.append(candidate)
            if 'web.app' not in mods:
                mods.append('web.app')
            return mods

        def _import_run_web_server() -> Callable[..., Any]:
            last_err: Optional[Exception] = None
            for mod_name in _candidate_modules():
                try:
                    module = importlib.import_module(mod_name)
                    fn = getattr(module, 'run_web_server', None)
                    if callable(fn):
                        return fn
                except Exception as e:
                    last_err = e
                    continue
            if last_err:
                raise ImportError(
                    'Unable to import run_web_server from candidate modules') from last_err
            raise ImportError('Unable to locate run_web_server')

        run_web_server = _import_run_web_server()

        try:
            run_web_server(app_context=app_context, host=host,
                           debug=debug, threads=threads)
        except RuntimeError:
            logger.exception(
                'Web UI failed to start due to a runtime configuration error')
            raise
        except ImportError:
            logger.exception('Web UI failed to start due to import error')
            raise
        except Exception:
            logger.exception(
                'Web UI failed to start due to an unexpected error')
            raise

    def get_web_ui_pid_path(self) -> str:
        '''Returns the absolute path to the PID file for the detached Web UI server.
        The PID file is typically stored in the application's configuration directory
        (:attr:`._config_dir`) with the filename defined by
        :attr:`._WEB_SERVER_PID_FILENAME`.
        Returns:
            str: The absolute path to the Web UI's PID file.
        '''
        config_dir = getattr(self, '_config_dir', None)
        filename = getattr(self, '_WEB_SERVER_PID_FILENAME', None)
        if not config_dir or not filename:
            raise RuntimeError(
                'Configuration directory or PID filename is not configured')
        return os.path.abspath(os.path.join(config_dir, filename))

    def get_web_ui_expected_start_arg(self) -> List[str]:
        '''Returns the list of arguments used to identify a detached Web UI server process.
        These arguments (defined by :attr:`._WEB_SERVER_START_ARG`) are typically
        used by process management utilities to find and identify the correct
        Web UI server process when it's run in a detached or background mode.
        Returns:
            List[str]: A list of command-line arguments.
        '''
        args = getattr(self, '_WEB_SERVER_START_ARG', None)
        if args is None:
            raise RuntimeError('Web server start arguments are not configured')
        if isinstance(args, str):
            return [args]
        if isinstance(args, (list, tuple)):
            return list(args)
        raise TypeError(
            'Web server start arguments must be a string or list of strings')

    def get_web_ui_executable_path(self) -> str:
        '''Returns the path to the main application executable used for starting the Web UI.
        This path, stored in :attr:`._expath`, is essential for constructing
        commands to start the Web UI, especially for system services.
        Returns:
            str: The path to the application executable.
        Raises:
            ConfigurationError: If the application executable path (:attr:`._expath`)
                is not configured or is empty.
        '''
        try:
            # Prefer a project-defined ConfigurationError if available
            from .exceptions import ConfigurationError  # type: ignore
        except Exception:
            class ConfigurationError(Exception):  # type: ignore
                pass
        expath = getattr(self, '_expath', None)
        if not expath or not str(expath).strip():
            raise ConfigurationError(
                'Application executable path (_expath) is not configured')
        return str(expath)
