
import os
import subprocess
from typing import Optional, Union, List, Any


class WebProcessMixin:
    """
    Mixin providing utilities to start a web UI process directly and
    to retrieve related paths and arguments.
    """

    def start_web_ui_direct(
        self,
        app_context: Any,
        host: Optional[Union[str, List[str]]] = None,
        debug: bool = False,
        threads: Optional[int] = None,
    ) -> None:
        """
        Start the web UI process directly using subprocess.

        Parameters
        ----------
        app_context : Any
            Application context object. It is not used directly in this
            implementation but is kept for compatibility with the
            original signature.
        host : str | list[str] | None, optional
            Host(s) to bind the web UI to. If a list is provided, the
            hosts are joined with commas.
        debug : bool, optional
            Enable debug mode.
        threads : int | None, optional
            Number of worker threads to use.
        """
        # Resolve executable path
        executable = self.get_web_ui_executable_path()

        # Base arguments
        args: List[str] = [executable] + self.get_web_ui_expected_start_arg()

        # Optional arguments
        if host is not None:
            if isinstance(host, list):
                host_str = ",".join(host)
            else:
                host_str = host
            args.extend(["--host", host_str])

        if debug:
            args.append("--debug")

        if threads is not None:
            args.extend(["--threads", str(threads)])

        # Start the process
        process = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Write the PID to the pid file
        pid_path = self.get_web_ui_pid_path()
        try:
            with open(pid_path, "w") as f:
                f.write(str(process.pid))
        except OSError:
            # If we cannot write the PID file, terminate the process
            process.terminate()
            raise

    def get_web_ui_pid_path(self) -> str:
        """
        Return the path to the PID file used by the web UI process.
        """
        # Use a temporary directory for the PID file
        return os.path.join(os.path.dirname(__file__), "web_ui.pid")

    def get_web_ui_expected_start_arg(self) -> List[str]:
        """
        Return the list of arguments that are expected to start the web UI.
        """
        # Default start argument; can be overridden by subclasses
        return ["--start"]

    def get_web_ui_executable_path(self) -> str:
        """
        Return the absolute path to the web UI executable.
        """
        # Assume the executable is located in the same directory as this file
        return os.path.join(os.path.dirname(__file__), "web_ui_executable")
