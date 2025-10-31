
import subprocess
from pathlib import Path
from typing import Union, Optional, Dict, List
from subprocess import CompletedProcess


class App:

    def __init__(self, path: Path) -> None:
        self.path = path

    def run_command(
        self,
        cmd: Union[str, List[str]],
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[Path] = None,
        *,
        debug: bool = False,
        echo: bool = False,
        quiet: bool = False,
        check: bool = False,
        command_borders: bool = False
    ) -> CompletedProcess[str]:

        if isinstance(cmd, str):
            cmd = [cmd]

        if cwd is None:
            cwd = self.path

        if echo:
            print(f"Running command: {' '.join(cmd)}")

        if command_borders:
            print("=" * 40)
            print(f"Running command: {' '.join(cmd)}")
            print("=" * 40)

        result = subprocess.run(
            cmd,
            env=env,
            cwd=cwd,
            capture_output=not debug,
            text=True,
            check=check
        )

        if not quiet and not debug:
            print(result.stdout)
            if result.stderr:
                print(result.stderr)

        return result
