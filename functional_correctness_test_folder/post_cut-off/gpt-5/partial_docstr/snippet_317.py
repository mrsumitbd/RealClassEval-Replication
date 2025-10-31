from typing import Optional, Union, List, Any, Dict

import os
import inspect


class ConfigurationError(RuntimeError):
    pass


class WebProcessMixin:

    def start_web_ui_direct(self, app_context: "AppContext", host: Optional[Union[str, List[str]]] = None, debug: bool = False, threads: Optional[int] = None) -> None:
        kwargs: Dict[str, Any] = {}
        if host is not None:
            kwargs["host"] = host
        kwargs["debug"] = bool(debug)
        if threads is not None:
            kwargs["threads"] = threads

        candidate_methods = (
            "start_web_ui",
            "run_web_ui",
            "run_server",
            "serve",
            "start",
        )

        for name in candidate_methods:
            func = getattr(app_context, name, None)
            if callable(func):
                try:
                    sig = inspect.signature(func)
                    bound = {}  # filter kwargs to what the function accepts
                    for k, v in kwargs.items():
                        if k in sig.parameters:
                            bound[k] = v
                    func(**bound)
                    return
                except TypeError:
                    # Fallback: try calling without filtering if signature mismatched
                    func(**kwargs)
                    return

        raise RuntimeError(
            "No suitable method found on app_context to start the Web UI. Tried: " + ", ".join(candidate_methods))

    def get_web_ui_pid_path(self) -> str:
        if not hasattr(self, "_config_dir") or not self._config_dir:
            raise ConfigurationError(
                "Configuration directory (_config_dir) is not set.")
        if not hasattr(self, "_WEB_SERVER_PID_FILENAME") or not self._WEB_SERVER_PID_FILENAME:
            raise ConfigurationError(
                "Web server PID filename (_WEB_SERVER_PID_FILENAME) is not set.")
        base = os.path.expanduser(str(self._config_dir))
        filename = str(self._WEB_SERVER_PID_FILENAME)
        path = os.path.abspath(os.path.join(base, filename))
        return path

    def get_web_ui_expected_start_arg(self) -> List[str]:
        if not hasattr(self, "_WEB_SERVER_START_ARG") or self._WEB_SERVER_START_ARG is None:
            raise ConfigurationError(
                "Expected start argument (_WEB_SERVER_START_ARG) is not set.")
        arg = self._WEB_SERVER_START_ARG
        if isinstance(arg, str):
            arg_list = [arg]
        elif isinstance(arg, (list, tuple)):
            arg_list = list(arg)
        else:
            raise ConfigurationError(
                "Expected start argument (_WEB_SERVER_START_ARG) must be a string or list of strings.")
        if not arg_list or any(not isinstance(x, str) or not x for x in arg_list):
            raise ConfigurationError(
                "Expected start argument list is empty or contains invalid items.")
        return arg_list

    def get_web_ui_executable_path(self) -> str:
        if not hasattr(self, "_expath") or self._expath is None:
            raise ConfigurationError(
                "Application executable path (_expath) is not configured.")
        expath = str(self._expath).strip()
        if not expath:
            raise ConfigurationError(
                "Application executable path (_expath) is empty.")
        expath = os.path.abspath(os.path.expanduser(expath))
        return expath
