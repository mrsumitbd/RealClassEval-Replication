
import subprocess
from pathlib import Path
from subprocess import CompletedProcess


class App:

    def __init__(self, path: Path) -> None:
        self.path = path

    def run_command(self, cmd: str | list[str], env: dict[str, str] | None = None, cwd: Path | None = None, *, debug: bool = False, echo: bool = False, quiet: bool = False, check: bool = False, command_borders: bool = False) -> CompletedProcess[str]:
        if command_borders:
            print("=" * 80)

        if echo:
            print(f"Running command: {cmd}")

        if cwd is None:
            cwd = self.path

        result = subprocess.run(cmd, env=env, cwd=cwd,
                                capture_output=True, text=True, check=check)

        if debug:
            print(f"Command output: {result.stdout}")
            print(f"Command error: {result.stderr}")

        if not quiet:
            print(result.stdout)

        if command_borders:
            print("=" * 80)

        return result
