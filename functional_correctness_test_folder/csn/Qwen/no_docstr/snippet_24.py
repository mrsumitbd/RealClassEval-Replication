
from pathlib import Path
from subprocess import run, CompletedProcess


class App:

    def __init__(self, path: Path) -> None:
        self.path = path

    def run_command(self, cmd: str | list[str], env: dict[str, str] | None = None, cwd: Path | None = None, *, debug: bool = False, echo: bool = False, quiet: bool = False, check: bool = False, command_borders: bool = False) -> CompletedProcess[str]:
        if cwd is None:
            cwd = self.path
        if echo:
            print(f"Running command: {cmd}")
        if command_borders:
            print("----- COMMAND START -----")
        result = run(cmd, env=env, cwd=cwd,
                     capture_output=not quiet, text=True, check=check)
        if command_borders:
            print("----- COMMAND END -----")
        if debug:
            print(f"Command output: {result.stdout}")
            print(f"Command error: {result.stderr}")
        return result
