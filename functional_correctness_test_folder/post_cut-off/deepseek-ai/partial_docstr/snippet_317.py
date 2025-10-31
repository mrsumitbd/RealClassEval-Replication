
import os
from typing import Optional, Union, List


class WebProcessMixin:

    def start_web_ui_direct(self, app_context: AppContext, host: Optional[Union[str, List[str]]] = None, debug: bool = False, threads: Optional[int] = None) -> None:
        pass

    def get_web_ui_pid_path(self) -> str:
        return os.path.join(self._config_dir, self._WEB_SERVER_PID_FILENAME)

    def get_web_ui_expected_start_arg(self) -> List[str]:
        return self._WEB_SERVER_START_ARG

    def get_web_ui_executable_path(self) -> str:
        if not hasattr(self, '_expath') or not self._expath:
            raise ConfigurationError(
                "The application executable path is not configured or is empty.")
        return self._expath
