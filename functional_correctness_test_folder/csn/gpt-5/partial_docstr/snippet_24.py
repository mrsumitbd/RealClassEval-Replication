from __future__ import annotations

import os
import shlex
import subprocess
import sys
from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess


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
        if isinstance(cmd, str):
            cmd_for_display = cmd
            use_shell = True
            run_cmd: str | list[str] = cmd
        else:
            try:
                cmd_for_display = shlex.join(cmd)
            except Exception:
                cmd_for_display = " ".join(shlex.quote(c) for c in cmd)
            use_shell = False
            run_cmd = cmd

        run_cwd = Path(cwd) if cwd is not None else self.path

        base_env = os.environ.copy()
        if env:
            base_env.update(env)

        if echo:
            print(f"$ {cmd_for_display}",
                  file=sys.stderr if quiet else sys.stdout)

        if debug:
            print(f"[debug] cwd: {run_cwd}", file=sys.stderr)
            if env:
                print(
                    f"[debug] env overrides: {', '.join(sorted(env.keys()))}", file=sys.stderr)

        # If we want borders, we must capture output to print inside borders, and
        # then optionally raise if check=True.
        if command_borders and not quiet:
            proc = subprocess.run(
                run_cmd,
                shell=use_shell,
                cwd=str(run_cwd) if run_cwd is not None else None,
                env=base_env,
                text=True,
                capture_output=True,
                check=False,
            )
            border = "=" * 8
            print(f"{border} BEGIN: {cmd_for_display} {border}")
            if proc.stdout:
                print(proc.stdout, end="" if proc.stdout.endswith("\n") else "\n")
            if proc.stderr:
                # Label stderr to distinguish, only if non-empty
                print("--- stderr ---")
                print(proc.stderr, end="" if proc.stderr.endswith("\n") else "\n")
            print(f"{border} END ({proc.returncode}): {cmd_for_display} {border}")

            if check and proc.returncode != 0:
                raise CalledProcessError(
                    proc.returncode, run_cmd, output=proc.stdout, stderr=proc.stderr)

            return proc

        # Without borders, decide output handling based on quiet
        stdout_setting = subprocess.DEVNULL if quiet else None
        stderr_setting = subprocess.DEVNULL if quiet else None

        proc = subprocess.run(
            run_cmd,
            shell=use_shell,
            cwd=str(run_cwd) if run_cwd is not None else None,
            env=base_env,
            text=True,
            stdout=stdout_setting,
            stderr=stderr_setting,
            check=check,
        )
        return proc
