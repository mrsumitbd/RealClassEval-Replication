class WebProcessMixin:
    '''
    Mixin class for BedrockServerManager that handles direct Web UI process management.
        '''

    def start_web_ui_direct(self, app_context: AppContext, host: Optional[Union[str, List[str]]] = None, debug: bool = False, threads: Optional[int] = None) -> None:
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
        try:
            # Prefer relative import within the package
            from .web.app import run_web_server  # type: ignore
        except Exception as e:
            # Fallback: attempt dynamic relative import using importlib
            import importlib
            try:
                mod = importlib.import_module('.web.app', package=__package__)
                run_web_server = getattr(mod, 'run_web_server')
            except Exception as ex:
                raise ImportError(
                    "Failed to import '.web.app.run_web_server'") from ex
        # Call the server runner; let exceptions propagate as documented
        kwargs = {'app_context': app_context, 'host': host, 'debug': debug}
        if threads is not None:
            kwargs['threads'] = threads
        run_web_server(**kwargs)

    def get_web_ui_pid_path(self) -> str:
        '''Returns the absolute path to the PID file for the detached Web UI server.
        The PID file is typically stored in the application's configuration directory
        (:attr:`._config_dir`) with the filename defined by
        :attr:`._WEB_SERVER_PID_FILENAME`.
        Returns:
            str: The absolute path to the Web UI's PID file.
        '''
        import os
        config_dir = getattr(self, '_config_dir', None)
        pid_filename = getattr(self, '_WEB_SERVER_PID_FILENAME', None)
        if not config_dir or not pid_filename:
            raise RuntimeError(
                'Configuration directory or PID filename is not configured.')
        return os.path.abspath(os.path.join(str(config_dir), str(pid_filename)))

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
            return []
        if isinstance(args, (list, tuple)):
            return list(args)
        if isinstance(args, str):
            return [args]
        return [str(args)]

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
        expath = getattr(self, '_expath', None)
        if not expath:
            try:
                from .exceptions import ConfigurationError  # type: ignore
            except Exception:
                raise RuntimeError(
                    'Application executable path (_expath) is not configured.')
            raise ConfigurationError(
                'Application executable path (_expath) is not configured.')
        return str(expath)
