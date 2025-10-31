
import subprocess
from pathlib import Path
from typing import Union

CompletedProcess = subprocess.CompletedProcess


class App:

    def __init__(self, path: Path) -> None:
        self.path = path

    def run_command(self, cmd: Union[str, list[str]], env: dict[str, str] | None = None, cwd: Path | None = None, *, debug: bool = False, echo: bool = False, quiet: bool = False, check: bool = False, command_borders: bool = False) -> CompletedProcess[str]:
        if isinstance(cmd, str):
            cmd_list = cmd.split()
        else:
            cmd_list = cmd

        if cwd is None:
            cwd = self.path

        if env is None:
            env = {}

        env = {**dict(subprocess.os.environ), **env}

        if command_borders:
            print("-" * 80)

        if debug or echo:
            print(f"Running command: {' '.join(cmd_list)}")
            if cwd:
                print(f"In directory: {cwd}")

        try:
            result = subprocess.run(cmd_list, env=env, cwd=str(
                cwd), check=check, capture_output=not echo, text=True)
        except subprocess.CalledProcessError as e:
            if not quiet:
                print(f"Command failed with return code {e.returncode}")
            raise

        if debug and not quiet:
            print(f"Command output: {result.stdout}")
            if result.stderr:
                print(f"Command error: {result.stderr}")

        if command_borders:
            print("-" * 80)

        return result
