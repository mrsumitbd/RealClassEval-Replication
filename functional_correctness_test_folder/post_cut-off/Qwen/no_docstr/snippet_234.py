
from argparse import ArgumentParser
from typing import Callable, Dict, Any
import subprocess
import os
import shutil


class Build:

    def __init__(self) -> None:
        self.parser = self._set_up_parser()
        self.args = self.parser.parse_args()

    def _set_up_parser(self) -> ArgumentParser:
        parser = ArgumentParser(description="Build script for the project.")
        parser.add_argument('--clean', action='store_true',
                            help='Clean the build directory.')
        parser.add_argument('--build', action='store_true',
                            help='Build the project.')
        parser.add_argument('--venv', action='store_true',
                            help='Set up a virtual environment.')
        return parser

    def _run_command(self, cmd: str, method: Callable[[str], None] = None, **kwargs: Dict[str, Any]) -> int:
        try:
            result = subprocess.run(cmd, shell=True, check=True, **kwargs)
            if method:
                method(result.stdout.decode())
            return 0
        except subprocess.CalledProcessError:
            return 1

    def _set_up_venv(self) -> int:
        return self._run_command('python -m venv venv')

    def _build(self) -> int:
        return self._run_command('python setup.py build')

    def _clean(self) -> int:
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('venv'):
            shutil.rmtree('venv')
        return 0

    def main(self) -> int:
        if self.args.clean:
            return self._clean()
        if self.args.venv:
            return self._set_up_venv()
        if self.args.build:
            return self._build()
        return 1
