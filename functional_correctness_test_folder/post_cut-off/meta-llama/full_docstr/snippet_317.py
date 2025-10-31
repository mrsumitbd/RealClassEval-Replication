
import os
from typing import Optional, Union, List
import importlib


class ConfigurationError(Exception):
    pass


class AppContext:
    # Assuming AppContext is defined elsewhere
    pass


class WebProcessMixin:
    '''
    Mixin class for BedrockServerManager that handles direct Web UI process management.
    '''

    _WEB_SERVER_PID_FILENAME = 'web_ui.pid'
    _WEB_SERVER_START_ARG = ['--mode', 'detached']
    _config_dir = '/path/to/config/dir'  # Replace with actual config dir
    _expath = '/path/to/executable'  # Replace with actual executable path

    def start_web_ui_direct(self, app_context: AppContext, host: Optional[Union[str, List[str]]] = None, debug: bool = False, threads: Optional[int] = None) -> None:
        try:
            web_app_module = importlib.import_module(
                '.web.app', package='your_package_name')  # Replace 'your_package_name'
            run_web_server = getattr(web_app_module, 'run_web_server')
            run_web_server(host=host, debug=debug, threads=threads)
        except ImportError as e:
            raise ImportError(
                "Failed to import web application components") from e
        except RuntimeError as e:
            raise RuntimeError("Failed to start web server") from e
        except Exception as e:
            raise Exception("Failed to start web server") from e

    def get_web_ui_pid_path(self) -> str:
        return os.path.join(self._config_dir, self._WEB_SERVER_PID_FILENAME)

    def get_web_ui_expected_start_arg(self) -> List[str]:
        return self._WEB_SERVER_START_ARG

    def get_web_ui_executable_path(self) -> str:
        if not self._expath:
            raise ConfigurationError(
                "Application executable path is not configured")
        return self._expath
