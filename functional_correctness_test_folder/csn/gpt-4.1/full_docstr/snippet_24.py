
from pathlib import Path
from subprocess import run, CompletedProcess, CalledProcessError
import os
import shlex
import sys


class App:
    '''App class that keep runtime status.'''

    def __init__(self, path: Path) -> None:
        '''Create a new app instance.
        Args:
            path: The path to the project.
        '''
        self.path = Path(path)

    def run_command(
        self,
        cmd: str | list[str],
        env: dict[str, str] | None = None,
        cwd: Path | None = None,
        *,
        debug: bool = False,
        echo: bool = False,
        quiet: bool = False,
        check: bool = False,
        command_borders: bool = False
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
        # Prepare command
        if isinstance(cmd, str):
            shell = True
            cmd_str = cmd
            display_cmd = cmd
        else:
            shell = False
            cmd_str = ' '.join(shlex.quote(str(c)) for c in cmd)
            display_cmd = cmd_str

        # Prepare environment
        run_env = os.environ.copy()
        if env:
            run_env.update(env)

        # Prepare working directory
        run_cwd = str(cwd) if cwd else str(self.path)

        # Echo command if needed
        if echo or debug:
            print(f"$ {display_cmd}", file=sys.stderr)

        # Command borders
        if command_borders:
            border = "=" * 40
            print(border, file=sys.stderr)
            print(f"Running: {display_cmd}", file=sys.stderr)
            print(border, file=sys.stderr)

        # Run the command
        try:
            completed = run(
                cmd,
                shell=shell,
                env=run_env,
                cwd=run_cwd,
                capture_output=quiet,
                text=True,
                check=check
            )
        except CalledProcessError as e:
            if not quiet:
                if e.stdout:
                    print(e.stdout, end='', file=sys.stdout)
                if e.stderr:
                    print(e.stderr, end='', file=sys.stderr)
            if command_borders:
                print("=" * 40, file=sys.stderr)
            raise

        # Output if not quiet
        if not quiet:
            if completed.stdout:
                print(completed.stdout, end='', file=sys.stdout)
            if completed.stderr:
                print(completed.stderr, end='', file=sys.stderr)

        if command_borders:
            print("=" * 40, file=sys.stderr)

        return completed
