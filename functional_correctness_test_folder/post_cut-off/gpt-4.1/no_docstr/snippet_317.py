
import os
import sys
import subprocess
from typing import Optional, Union, List


class WebProcessMixin:
    def start_web_ui_direct(self, app_context, host: Optional[Union[str, List[str]]] = None, debug: bool = False, threads: Optional[int] = None) -> None:
        args = [sys.executable, self.get_web_ui_executable_path()]
        args += self.get_web_ui_expected_start_arg()
        if host:
            if isinstance(host, list):
                for h in host:
                    args += ["--host", h]
            else:
                args += ["--host", host]
        if debug:
            args.append("--debug")
        if threads is not None:
            args += ["--threads", str(threads)]
        pid_path = self.get_web_ui_pid_path()
        with open(pid_path, "w") as pid_file:
            proc = subprocess.Popen(args)
            pid_file.write(str(proc.pid))

    def get_web_ui_pid_path(self) -> str:
        return os.path.join(os.getcwd(), "web_ui.pid")

    def get_web_ui_expected_start_arg(self) -> List[str]:
        return ["run"]

    def get_web_ui_executable_path(self) -> str:
        return os.path.join(os.getcwd(), "web_ui.py")
