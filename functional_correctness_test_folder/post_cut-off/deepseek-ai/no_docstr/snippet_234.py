
import argparse
from argparse import ArgumentParser
from typing import Callable, Dict, Any
import subprocess
import sys
import venv


class Build:

    def __init__(self) -> None:
        self.parser = self._set_up_parser()

    def _set_up_parser(self) -> ArgumentParser:
        parser = argparse.ArgumentParser(description="Build tool")
        parser.add_argument("--clean", action="store_true",
                            help="Clean build artifacts")
        parser.add_argument("--no-venv", action="store_true",
                            help="Skip virtual environment setup")
        return parser

    def _run_command(self, cmd: str, method: Callable[[str], None] = None, **kwargs: Dict[str, Any]) -> int:
        try:
            result = subprocess.run(cmd, shell=True, check=True, **kwargs)
            if method:
                method(cmd)
            return 0
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {cmd}", file=sys.stderr)
            return e.returncode

    def _set_up_venv(self) -> int:
        try:
            venv.create("venv", with_pip=True)
            return 0
        except Exception as e:
            print(
                f"Failed to set up virtual environment: {e}", file=sys.stderr)
            return 1

    def _build(self) -> int:
        commands = [
            "pip install -r requirements.txt",
            "python setup.py build"
        ]
        for cmd in commands:
            ret = self._run_command(cmd)
            if ret != 0:
                return ret
        return 0

    def _clean(self) -> int:
        commands = [
            "rm -rf build",
            "rm -rf dist",
            "rm -rf *.egg-info"
        ]
        for cmd in commands:
            ret = self._run_command(cmd)
            if ret != 0:
                return ret
        return 0

    def main(self) -> int:
        args = self.parser.parse_args()

        if args.clean:
            return self._clean()

        if not args.no_venv:
            ret = self._set_up_venv()
            if ret != 0:
                return ret

        return self._build()
