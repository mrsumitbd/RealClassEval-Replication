
import subprocess
import sys
import os
import shutil
from argparse import ArgumentParser
from typing import Callable, Dict, Any


class Build:

    def __init__(self) -> None:
        self.parser = self._set_up_parser()
        self.args = None

    def _set_up_parser(self) -> ArgumentParser:
        parser = ArgumentParser(description="Build utility")
        parser.add_argument(
            "command",
            choices=["venv", "build", "clean"],
            help="Command to run: venv, build, clean"
        )
        return parser

    def _run_command(self, cmd: str, method: Callable[[str], None] = None, **kwargs: Dict[str, Any]) -> int:
        try:
            if method:
                method(cmd)
                return 0
            else:
                result = subprocess.run(cmd, shell=True, check=False, **kwargs)
                return result.returncode
        except Exception as e:
            print(f"Error running command: {cmd}\n{e}", file=sys.stderr)
            return 1

    def _set_up_venv(self) -> int:
        venv_dir = "venv"
        if os.path.exists(venv_dir):
            print("Virtual environment already exists.")
            return 0
        cmd = f"{sys.executable} -m venv {venv_dir}"
        return self._run_command(cmd)

    def _build(self) -> int:
        # Assume pyproject.toml exists and use build module if available
        if not os.path.exists("pyproject.toml"):
            print("pyproject.toml not found. Cannot build.", file=sys.stderr)
            return 1
        cmd = f"{sys.executable} -m build"
        return self._run_command(cmd)

    def _clean(self) -> int:
        # Remove build/, dist/, *.egg-info/
        dirs = ["build", "dist"]
        egg_info_dirs = [d for d in os.listdir(
            '.') if d.endswith('.egg-info') and os.path.isdir(d)]
        all_dirs = dirs + egg_info_dirs
        for d in all_dirs:
            if os.path.exists(d):
                try:
                    shutil.rmtree(d)
                    print(f"Removed {d}")
                except Exception as e:
                    print(f"Failed to remove {d}: {e}", file=sys.stderr)
                    return 1
        return 0

    def main(self) -> int:
        self.args = self.parser.parse_args()
        cmd = self.args.command
        if cmd == "venv":
            return self._set_up_venv()
        elif cmd == "build":
            return self._build()
        elif cmd == "clean":
            return self._clean()
        else:
            print(f"Unknown command: {cmd}", file=sys.stderr)
            return 1
