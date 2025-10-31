from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from typing import Iterable


class App:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)

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
        command_borders: bool = False,
    ) -> CompletedProcess[str]:
        use_shell = isinstance(cmd, str)
        run_cwd = Path(cwd) if cwd is not None else self.path

        base_env = os.environ.copy()
        if env:
            base_env.update(env)

        display_cmd: str
        if isinstance(cmd, str):
            display_cmd = cmd
        else:
            # best-effort shell-like representation
            try:
                display_cmd = shlex.join(cmd)
            except Exception:
                display_cmd = " ".join(cmd)

        def _print(line: str = "") -> None:
            if not quiet:
                print(line)

        if command_borders and not quiet:
            _print("=" * 80)
            _print(f"RUN: {display_cmd}")
            _print("- cwd: " + str(run_cwd))
            if debug:
                _print("- env overrides: " +
                       (", ".join(sorted(env.keys())) if env else "(none)"))
            _print("- shell: " + str(use_shell))
            _print("- check: " + str(check))
            _print("- echo: " + str(echo))
            _print("=" * 80)

        if echo and not quiet and not command_borders:
            _print(f"$ {display_cmd}")

        result = subprocess.run(
            cmd,
            shell=use_shell,
            cwd=str(run_cwd) if run_cwd is not None else None,
            env=base_env,
            text=True,
            capture_output=True,
            check=False,  # we'll handle check after printing
        )

        if not quiet:
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="", file=os.sys.stderr)

        if command_borders and not quiet:
            _print("")
            _print("=" * 80)
            _print(f"END (returncode={result.returncode})")
            _print("=" * 80)

        if check and result.returncode != 0:
            # Re-raise as CalledProcessError with captured output
            raise subprocess.CalledProcessError(
                result.returncode, cmd, output=result.stdout, stderr=result.stderr
            )

        return result
