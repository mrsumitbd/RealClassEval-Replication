
import os
import shlex
import subprocess
from pathlib import Path
from subprocess import CompletedProcess, CalledProcessError
from typing import Dict, List, Optional, Union


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
        command_borders: bool = False,
    ) -> CompletedProcess[str]:
        """
        Execute the given command and returns a CompletedProcess.
        """
        # Resolve command to list
        if isinstance(cmd, str):
            cmd_list = shlex.split(cmd)
        else:
            cmd_list = cmd

        # Merge environment
        env_combined = os.environ.copy()
        if env:
            env_combined.update(env)

        # Resolve working directory
        cwd_str = str(cwd) if cwd else None

        # Debug output
        if debug:
            print(f"[DEBUG] Running command: {cmd_list}")
            print(f"[DEBUG] Working directory: {cwd_str}")
            print(f"[DEBUG] Environment: {env_combined}")

        # Echo command
        if echo:
            print(f"Executing: {' '.join(cmd_list)}")

        # Run the command
        result = subprocess.run(
            cmd_list,
            cwd=cwd_str,
            env=env_combined,
            text=True,
            capture_output=True,
            check=check,
        )

        # Output handling
        if not quiet:
            if command_borders:
                print("-" * 80)
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="", file=os.sys.stderr)
            if command_borders:
                print("-" * 80)

        return result
