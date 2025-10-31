
from __future__ import annotations

import os
import subprocess
from pathlib import Path
from subprocess import CompletedProcess, CalledProcessError
from typing import Dict, Iterable, List, Optional, Union


class App:
    '''App class that keep runtime status.'''

    def __init__(self, path: Path) -> None:
        '''Create a new app instance.
        Args:
            path: The path to the project.
        '''
        self.path = path.resolve()
        self.env: Dict[str, str] = os.environ.copy()

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
        '''Execute the given command and returns None.
        Args:
            cmd: A list of strings containing the command to run.
            env: A dict containing the shell's environment.
            cwd: An optional Path to the working directory.
            debug: An optional bool to toggle debug output.
            echo: An optional bool to toggle command echo.
            quiet: An optional bool to toggle command output.
            check: An optional bool to toggle command error checking.
            command_borders: An optional bool to enable borders around command output.
        Returns:
            A completed process object.
        Raises:
            CalledProcessError: If return code is nonzero and check is True.
        '''
        # Resolve cwd
        run_cwd = str(cwd.resolve()) if cwd else None

        # Merge environment
        run_env = self.env.copy()
        if env:
            run_env.update(env)

        # Prepare command
        if isinstance(cmd, str):
            shell = True
            command_str = cmd
        else:
            shell = False
            command_str = " ".join(cmd)

        # Debug output
        if debug:
            print(f"[DEBUG] Running command: {command_str}")
            print(f"[DEBUG] CWD: {run_cwd or self.path}")
            print(f"[DEBUG] ENV: {run_env}")

        # Echo command
        if echo:
            print(f"$ {command_str}")

        # Execute
        result = subprocess.run(
            cmd,
            shell=shell,
            cwd=run_cwd,
            env=run_env,
            text=True,
            capture_output=True,
            check=check,
        )

        # Output handling
        if not quiet:
            if command_borders:
                print("-" * 40)
                print(result.stdout)
                print("-" * 40)
            else:
                print(result.stdout, end="")

        return result
