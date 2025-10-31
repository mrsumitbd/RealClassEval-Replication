
import os
from typing import Optional, Union, List


class ConfigurationError(Exception):
    pass


class WebProcessMixin:
    '''
    Mixin class for BedrockServerManager that handles direct Web UI process management.
    '''

    # These attributes are expected to be set by the inheriting class
    # _config_dir: str
    # _WEB_SERVER_PID_FILENAME: str
    # _WEB_SERVER_START_ARG: List[str]
    # _expath: str

    def start_web_ui_direct(self, app_context, host: Optional[Union[str, List[str]]] = None, debug: bool = False, threads: Optional[int] = None) -> None:
        '''Starts the Web UI application directly in the current process (blocking).'''
        try:
            from web.app import run_web_server
        except ImportError as e:
            raise ImportError(
                "Could not import 'web.app.run_web_server'.") from e

        try:
            run_web_server(
                app_context=app_context,
                host=host,
                debug=debug,
                threads=threads
            )
        except RuntimeError as e:
            raise RuntimeError("Web server failed to start: " + str(e)) from e
        except Exception as e:
            raise

    def get_web_ui_pid_path(self) -> str:
        '''Returns the absolute path to the PID file for the detached Web UI server.'''
        if not hasattr(self, "_config_dir") or not hasattr(self, "_WEB_SERVER_PID_FILENAME"):
            raise AttributeError(
                "Missing required attributes '_config_dir' or '_WEB_SERVER_PID_FILENAME'.")
        return os.path.abspath(os.path.join(self._config_dir, self._WEB_SERVER_PID_FILENAME))

    def get_web_ui_expected_start_arg(self) -> List[str]:
        '''Returns the list of arguments used to identify a detached Web UI server process.'''
        if not hasattr(self, "_WEB_SERVER_START_ARG"):
            raise AttributeError(
                "Missing required attribute '_WEB_SERVER_START_ARG'.")
        return list(self._WEB_SERVER_START_ARG)

    def get_web_ui_executable_path(self) -> str:
        '''Returns the path to the main application executable used for starting the Web UI.'''
        if not hasattr(self, "_expath") or not self._expath:
            raise ConfigurationError(
                "Application executable path (_expath) is not configured or is empty.")
        return self._expath
