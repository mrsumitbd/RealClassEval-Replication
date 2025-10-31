
import os
from typing import Optional, Union, List


class ConfigurationError(Exception):
    pass


class AppContext:
    # Dummy placeholder for type hinting
    pass


class WebProcessMixin:
    _config_dir: str = "/etc/myapp"
    _WEB_SERVER_PID_FILENAME: str = "webui.pid"
    _WEB_SERVER_START_ARG: List[str] = ["--web-ui", "--start"]
    _expath: Optional[str] = "/usr/local/bin/myapp"

    def start_web_ui_direct(self, app_context: AppContext, host: Optional[Union[str, List[str]]] = None, debug: bool = False, threads: Optional[int] = None) -> None:
        import subprocess
        args = [self.get_web_ui_executable_path()] + \
            self.get_web_ui_expected_start_arg()
        if host:
            if isinstance(host, list):
                for h in host:
                    args.extend(["--host", h])
            else:
                args.extend(["--host", host])
        if debug:
            args.append("--debug")
        if threads is not None:
            args.extend(["--threads", str(threads)])
        subprocess.Popen(args, cwd=self._config_dir)

    def get_web_ui_pid_path(self) -> str:
        return os.path.abspath(os.path.join(self._config_dir, self._WEB_SERVER_PID_FILENAME))

    def get_web_ui_expected_start_arg(self) -> List[str]:
        return list(self._WEB_SERVER_START_ARG)

    def get_web_ui_executable_path(self) -> str:
        if not self._expath or not str(self._expath).strip():
            raise ConfigurationError(
                "Application executable path (_expath) is not configured or is empty.")
        return str(self._expath)
