
from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any, Dict, Iterable, List, Optional, Union


class App:
    """
    Simple wrapper around subprocess.run that provides a few convenience options.
    """

    def __init__(self, path: Path) -> None:
        """
        Store the base path for the application.

        Parameters
        ----------
        path : Path
            The working directory for commands that do not specify a cwd.
        """
        self.path = path

    def run_command(
        self,
        cmd: Union[str, List[str]],
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[Path] = None,
        *,
        debug: bool = False,
        echo: bool = False,
        quiet: bool = False,
        check: bool = False,
        command_borders: bool = False,
    ) -> CompletedProcess[str]:
        """
        Execute a command with optional debugging, echoing, and output suppression.

        Parameters
        ----------
        cmd : str | list[str]
            The command to run. If a string, it will be executed through the shell.
        env : dict[str, str] | None
            Environment variables for the subprocess. If None, the current environment is used.
        cwd : Path | None
            Working directory for the subprocess. If None, ``self.path`` is used.
        debug : bool
            If True, print the command and environment before execution.
        echo : bool
            If True, print the command string before execution.
        quiet : bool
            If True, suppress stdout and stderr from the subprocess.
        check : bool
            If True, raise ``subprocess.CalledProcessError`` on non‑zero exit status.
        command_borders : bool
            If True, print start/end borders around the command execution.

        Returns
        -------
        CompletedProcess[str]
            The result of the subprocess execution.
        """
        # Resolve working directory
        run_cwd = cwd if cwd is not None else self.path

        # Resolve environment
        run_env = env if env is not None else os.environ.copy()

        # Prepare command
        if isinstance(cmd, str):
            # Use shell for string commands
            shell = True
            # For shell=True, we need a string
            cmd_str = cmd
        else:
            shell = False
            cmd_str = cmd

        # Debug output
        if debug:
            print("DEBUG: Running command:", cmd_str)
            print("DEBUG: Environment:", run_env)
            print("DEBUG: Working directory:", run_cwd)

        # Echo command
        if echo:
            print("Executing:", cmd_str)

        # Command borders
        if command_borders:
            print("=== COMMAND START ===")

        # Configure subprocess.run
        result = subprocess.run(
            cmd_str,
            shell=shell,
            cwd=run_cwd,
            env=run_env,
            capture_output=not quiet,
            text=True,
            check=check,
        )

        # Command borders end
        if command_borders:
            print("=== COMMAND END ===")

        return result
