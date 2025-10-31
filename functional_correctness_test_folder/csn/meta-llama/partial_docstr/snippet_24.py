
import subprocess
from pathlib import Path
from subprocess import CompletedProcess, CalledProcessError


class App:

    def __init__(self, path: Path) -> None:
        self.path = path

    def run_command(self, cmd: str | list[str], env: dict[str, str] | None = None, cwd: Path | None = None, *, debug: bool = False, echo: bool = False, quiet: bool = False, check: bool = False, command_borders: bool = False) -> CompletedProcess[str]:
        if isinstance(cmd, str):
            cmd = cmd.split()

        if cwd is None:
            cwd = self.path

        if env is None:
            env = {}

        env = {**dict(subprocess.os.environ), **env}

        if debug or echo:
            print(f"Running command: {' '.join(cmd)}")
            if command_borders:
                print("-" * 80)

        stdout = subprocess.PIPE if not quiet else None
        stderr = subprocess.PIPE if not quiet else None

        try:
            result = subprocess.run(cmd, env=env, cwd=str(
                cwd), check=check, stdout=stdout, stderr=stderr, text=True)
        except CalledProcessError as e:
            if command_borders and not quiet:
                print("-" * 80)
            raise e

        if command_borders and not quiet:
            print("-" * 80)

        return result
