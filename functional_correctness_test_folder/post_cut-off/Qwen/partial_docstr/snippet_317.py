
from typing import Optional, Union, List
import os


class WebProcessMixin:

    _config_dir = '/path/to/config'
    _WEB_SERVER_PID_FILENAME = 'web_ui.pid'
    _WEB_SERVER_START_ARG = ['--web-ui']
    _expath = '/path/to/executable'

    def start_web_ui_direct(self, app_context: 'AppContext', host: Optional[Union[str, List[str]]] = None, debug: bool = False, threads: Optional[int] = None) -> None:
        import subprocess
        args = [self.get_web_ui_executable_path()]
        if host:
            args.extend(['--host', str(host)])
        if debug:
            args.append('--debug')
        if threads:
            args.extend(['--threads', str(threads)])
        subprocess.Popen(args)

    def get_web_ui_pid_path(self) -> str:
        return os.path.join(self._config_dir, self._WEB_SERVER_PID_FILENAME)

    def get_web_ui_expected_start_arg(self) -> List[str]:
        return self._WEB_SERVER_START_ARG

    def get_web_ui_executable_path(self) -> str:
        if not self._expath:
            raise ConfigurationError(
                "Application executable path is not configured or is empty.")
        return self._expath


class ConfigurationError(Exception):
    pass
