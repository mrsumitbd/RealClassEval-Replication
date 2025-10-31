
import subprocess
from pathlib import Path
from subprocess import CompletedProcess, CalledProcessError
from typing import Union, Optional


class App:
    '''App class that keep runtime status.'''

    def __init__(self, path: Path) -> None:
        '''Create a new app instance.
        Args:
            path: The path to the project.
        '''
        self.path = path

    def run_command(self, cmd: Union[str, list[str]], env: Optional[dict[str, str]] = None, cwd: Optional[Path] = None, *, debug: bool = False, echo: bool = False, quiet: bool = False, check: bool = False, command_borders: bool = False) -> CompletedProcess[str]:
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
        if isinstance(cmd, str):
            cmd = [cmd]

        if cwd is None:
            cwd = self.path

        if command_borders:
            print("=" * 40)

        if echo or debug:
            print(f"Running command: {' '.join(cmd)}")

        if debug:
            print(f"Working directory: {cwd}")
            if env:
                print(f"Environment: {env}")

        result = subprocess.run(
            cmd,
            env=env,
            cwd=cwd,
            text=True,
            capture_output=quiet,
            check=check
        )

        if command_borders:
            print("=" * 40)

        return result
