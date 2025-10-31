
from pathlib import Path
from subprocess import run, CompletedProcess, CalledProcessError
import os


class App:

    def __init__(self, path: Path) -> None:
        self.path = path

    def run_command(self, cmd: str | list[str], env: dict[str, str] | None = None, cwd: Path | None = None, *, debug: bool = False, echo: bool = False, quiet: bool = False, check: bool = False, command_borders: bool = False) -> CompletedProcess[str]:
        if isinstance(cmd, str):
            cmd = [cmd]

        if env is None:
            env = os.environ.copy()
        else:
            env = {**os.environ, **env}

        if cwd is None:
            cwd = self.path

        if echo:
            print(f"Executing: {' '.join(cmd)}")

        try:
            result = run(cmd, env=env, cwd=cwd,
                         capture_output=not quiet, text=True, check=check)
        except CalledProcessError as e:
            if debug:
                print(f"Error executing command: {e}")
            raise

        if command_borders:
            print("-" * 40)
            print(result.stdout)
            print("-" * 40)
        else:
            print(result.stdout)

        return result
