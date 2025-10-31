
import subprocess
from pathlib import Path
from typing import Union, Optional


class App:
    '''App class that keep runtime status.'''

    def __init__(self, path: Path) -> None:
        '''Create a new app instance.
        Args:
            path: The path to the project.
        '''
        self.path = path

    def run_command(self, cmd: Union[str, list[str]], env: Optional[dict[str, str]] = None, cwd: Optional[Path] = None, *, debug: bool = False, echo: bool = False, quiet: bool = False, check: bool = False, command_borders: bool = False) -> subprocess.CompletedProcess[str]:
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
            cmd_str = cmd
            cmd_list = ['/bin/sh', '-c', cmd]
        else:
            cmd_str = ' '.join(cmd)
            cmd_list = cmd

        if debug:
            print(f'DEBUG: Running command: {cmd_str}')

        if echo:
            if command_borders:
                print('=' * 80)
            print(f'$ {cmd_str}')
            if command_borders:
                print('-' * 80)

        result = subprocess.run(
            cmd_list,
            env=env,
            cwd=str(cwd or self.path),
            capture_output=quiet,
            check=check,
            text=True
        )

        if debug:
            print(f'DEBUG: Command return code: {result.returncode}')

        return result
