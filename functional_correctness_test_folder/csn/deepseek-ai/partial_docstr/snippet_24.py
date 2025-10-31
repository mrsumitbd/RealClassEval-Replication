
import subprocess
from pathlib import Path
from typing import Optional, Union


class App:

    def __init__(self, path: Path) -> None:
        self.path = path

    def run_command(
        self,
        cmd: Union[str, list[str]],
        env: Optional[dict[str, str]] = None,
        cwd: Optional[Path] = None,
        *,
        debug: bool = False,
        echo: bool = False,
        quiet: bool = False,
        check: bool = False,
        command_borders: bool = False
    ) -> subprocess.CompletedProcess[str]:
        if isinstance(cmd, str):
            cmd = [cmd]

        if debug:
            print(f"Debug: Running command: {cmd}")

        if echo:
            print(f"$ {' '.join(cmd)}")

        if command_borders:
            print("=" * 40)

        result = subprocess.run(
            cmd,
            env=env,
            cwd=str(cwd) if cwd else None,
            capture_output=quiet,
            text=True,
            check=check
        )

        if command_borders:
            print("=" * 40)

        return result
