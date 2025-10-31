
import os
from typing import Optional, Union, List


class ConfigurationError(Exception):
    pass


class AppContext:
    # Assuming AppContext is defined elsewhere
    pass


class WebProcessMixin:
    _WEB_SERVER_PID_FILENAME = 'web_ui.pid'
    _WEB_SERVER_START_ARG = ['--web-ui']

    def __init__(self, _config_dir: str, _expath: str):
        self._config_dir = _config_dir
        self._expath = _expath

    def start_web_ui_direct(self, app_context: AppContext, host: Optional[Union[str, List[str]]] = None, debug: bool = False, threads: Optional[int] = None) -> None:
        import subprocess
        command = [self.get_web_ui_executable_path()]
        if isinstance(host, list):
            for h in host:
                command.extend(['--host', h])
        elif host is not None:
            command.extend(['--host', host])
        if debug:
            command.append('--debug')
        if threads is not None:
            command.extend(['--threads', str(threads)])
        subprocess.Popen(command)

    def get_web_ui_pid_path(self) -> str:
        return os.path.join(self._config_dir, self._WEB_SERVER_PID_FILENAME)

    def get_web_ui_expected_start_arg(self) -> List[str]:
        return self._WEB_SERVER_START_ARG

    def get_web_ui_executable_path(self) -> str:
        if not self._expath:
            raise ConfigurationError(
                "Application executable path is not configured or is empty.")
        return self._expath
