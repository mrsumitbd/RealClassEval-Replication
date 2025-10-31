
from pathlib import Path
from subprocess import run, CompletedProcess
import shlex
import os
from typing import Any


class App:
    def __init__(self, path: Path) -> None:
        self.path = path

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
        # Prepare command
        if isinstance(cmd, str):
            cmd_list = shlex.split(cmd)
            cmd_str = cmd
        else:
            cmd_list = cmd
            cmd_str = " ".join(shlex.quote(arg) for arg in cmd)

        # Prepare environment
        run_env = os.environ.copy()
        if env:
            run_env.update(env)

        # Prepare working directory
        run_cwd = str(cwd if cwd is not None else self.path)

        # Borders
        if command_borders:
            border = "=" * 40
            print(border)
            print(f"Running command: {cmd_str}")
            print(border)

        # Echo
        if echo:
            print(f"$ {cmd_str}")

        # Debug
        if debug:
            print(f"Command: {cmd_list}")
            print(f"Env: {env}")
            print(f"CWD: {run_cwd}")

        # Run command
        result = run(
            cmd_list,
            env=run_env,
            cwd=run_cwd,
            capture_output=quiet,
            text=True,
            check=check
        )

        # Output
        if not quiet:
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="", file=os.sys.stderr)

        if command_borders:
            print("=" * 40)

        return result
