
import subprocess
from pathlib import Path
from subprocess import CompletedProcess


class App:

    def __init__(self, path: Path) -> None:
        self.path = path

    def run_command(self, cmd: str | list[str], env: dict[str, str] | None = None, cwd: Path | None = None, *, debug: bool = False, echo: bool = False, quiet: bool = False, check: bool = False, command_borders: bool = False) -> CompletedProcess[str]:
        if isinstance(cmd, str):
            cmd = [cmd]

        if cwd is None:
            cwd = self.path

        if echo:
            print(f"Running command: {' '.join(cmd)}")

        if debug:
            print(f"Environment: {env}")
            print(f"Working directory: {cwd}")

        if command_borders:
            print("=" * 80)

        result = subprocess.run(cmd, env=env, cwd=cwd,
                                capture_output=not quiet, text=True)

        if command_borders:
            print("=" * 80)

        if check and result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode, cmd, result.stdout, result.stderr)

        return result
