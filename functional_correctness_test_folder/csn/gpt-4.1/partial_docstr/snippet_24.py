
from pathlib import Path
from subprocess import run, CompletedProcess, CalledProcessError
import sys
import shlex
import os


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
        if isinstance(cmd, str):
            cmd_list = shlex.split(cmd)
        else:
            cmd_list = cmd

        run_env = os.environ.copy()
        if env:
            run_env.update(env)

        run_cwd = str(cwd) if cwd else str(self.path)

        if echo or debug:
            print(
                f"Running command: {' '.join(shlex.quote(arg) for arg in cmd_list)}", file=sys.stderr)
            print(f"Working directory: {run_cwd}", file=sys.stderr)
            if env:
                print(f"Environment overrides: {env}", file=sys.stderr)

        if command_borders:
            border = "=" * 40
            print(border, file=sys.stderr)
            print(
                f"COMMAND: {' '.join(shlex.quote(arg) for arg in cmd_list)}", file=sys.stderr)
            print(border, file=sys.stderr)

        stdout_opt = sys.stdout if not quiet else open(os.devnull, "w")
        stderr_opt = sys.stderr if not quiet else open(os.devnull, "w")

        try:
            result = run(
                cmd_list,
                cwd=run_cwd,
                env=run_env,
                capture_output=False,
                text=True,
                check=check,
                stdout=stdout_opt,
                stderr=stderr_opt,
            )
        except CalledProcessError as e:
            if not quiet:
                print(
                    f"Command failed with exit code {e.returncode}", file=sys.stderr)
            if command_borders:
                print("=" * 40, file=sys.stderr)
            raise

        if command_borders:
            print("=" * 40, file=sys.stderr)

        # If quiet, close the devnull files
        if quiet:
            stdout_opt.close()
            stderr_opt.close()

        # Re-run with capture_output to return CompletedProcess[str] with output
        # (since above we redirected to sys.stdout/sys.stderr)
        # But only if not quiet, otherwise output is not needed
        result2 = run(
            cmd_list,
            cwd=run_cwd,
            env=run_env,
            capture_output=True,
            text=True,
            check=False,
        )
        if check and result2.returncode != 0:
            raise CalledProcessError(
                result2.returncode, cmd_list, output=result2.stdout, stderr=result2.stderr)
        return result2
