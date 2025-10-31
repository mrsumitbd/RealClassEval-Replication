
import os
import subprocess
from pathlib import Path
from typing import List, Optional, Union

# Minimal ConfigurationError definition for this mixin


class ConfigurationError(RuntimeError):
    """Raised when a required configuration value is missing or invalid."""
    pass


class WebProcessMixin:
    """
    Mixin providing utilities for starting and managing a detached Web UI server.
    """

    # These attributes are expected to be defined by the consuming class.
    _config_dir: Path  # Directory where configuration files are stored
    _WEB_SERVER_PID_FILENAME: str  # Name of the PID file
    # Arguments that identify the web server process
    _WEB_SERVER_START_ARG: List[str]
    _expath: str  # Path to the main application executable

    def start_web_ui_direct(
        self,
        app_context: "AppContext",
        host: Optional[Union[str, List[str]]] = None,
        debug: bool = False,
        threads: Optional[int] = None,
    ) -> None:
        """
        Start the Web UI directly (foreground) using the provided application context.

        Parameters
        ----------
        app_context : AppContext
            The application context providing configuration and environment.
        host : str | list[str] | None, optional
            Host(s) to bind the web server to. If a list is provided, the first
            element is used as the primary host.
        debug : bool, optional
            Enable debug mode for the web server.
        threads : int | None, optional
            Number of worker threads for the web server.

        Raises
        ------
        ConfigurationError
            If the executable path is not configured.
        RuntimeError
            If the subprocess fails to start.
        """
        # Resolve the executable path
        exe_path = self.get_web_ui_executable_path()

        # Build command arguments
        cmd: List[str] = [exe_path, "--web-ui"]

        # Host handling
        if host:
            if isinstance(host, list):
                # Use the first host in the list
                host = host[0]
            cmd.extend(["--host", str(host)])

        # Debug flag
        if debug:
            cmd.append("--debug")

        # Threads
        if threads is not None:
            cmd.extend(["--threads", str(threads)])

        # Append any additional arguments defined by the mixin
        cmd.extend(self.get_web_ui_expected_start_arg())

        # Start the process
        try:
            # Use the app_context's environment if available
            env = getattr(app_context, "env", os.environ.copy())
            subprocess.Popen(
                cmd,
                cwd=app_context.root_dir if hasattr(
                    app_context, "root_dir") else None,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to start Web UI: {exc}") from exc

    def get_web_ui_pid_path(self) -> str:
        """
        Returns the absolute path to the PID file for the detached Web UI server.

        Returns
        -------
        str
            The absolute path to the Web UI's PID file.
        """
        if not hasattr(self, "_config_dir") or not isinstance(self._config_dir, Path):
            raise ConfigurationError(
                "Configuration directory (_config_dir) is not set.")
        if not hasattr(self, "_WEB_SERVER_PID_FILENAME"):
            raise ConfigurationError(
                "PID filename (_WEB_SERVER_PID_FILENAME) is not set.")
        return str(self._config_dir / self._WEB_SERVER_PID_FILENAME)

    def get_web_ui_expected_start_arg(self) -> List[str]:
        """
        Returns the list of arguments used to identify a detached Web UI server process.

        Returns
        -------
        List[str]
            A list of command-line arguments.
        """
        if not hasattr(self, "_WEB_SERVER_START_ARG"):
            raise ConfigurationError(
                "Start arguments (_WEB_SERVER_START_ARG) are not set.")
        return list(self._WEB_SERVER_START_ARG)

    def get_web_ui_executable_path(self) -> str:
        """
        Returns the path to the main application executable used for starting the Web UI.

        Returns
        -------
        str
            The path to the application executable.

        Raises
        ------
        ConfigurationError
            If the application executable path (_expath) is not configured or is empty.
        """
        if not hasattr(self, "_expath") or not self._expath:
            raise ConfigurationError(
                "Executable path (_expath) is not configured.")
        return str(Path(self._expath).resolve())
