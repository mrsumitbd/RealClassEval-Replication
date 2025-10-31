
import subprocess
from argparse import ArgumentParser
from typing import Callable, Dict, Any


class Build:

    def __init__(self) -> None:
        self.parser = self._set_up_parser()

    def _set_up_parser(self) -> ArgumentParser:
        parser = ArgumentParser(description='Build and clean project.')
        parser.add_argument('--build', action='store_true',
                            help='Build the project.')
        parser.add_argument('--clean', action='store_true',
                            help='Clean the project.')
        return parser

    def _run_command(self, cmd: str, method: Callable[[str], None] = None, **kwargs: Dict[str, Any]) -> int:
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
        stdout, stderr = process.communicate()
        if method:
            method(stdout.decode('utf-8'))
        return process.returncode

    def _set_up_venv(self) -> int:
        return self._run_command('python -m venv venv')

    def _build(self) -> int:
        return self._run_command('python setup.py build')

    def _clean(self) -> int:
        return self._run_command('python setup.py clean --all')

    def main(self) -> int:
        args = self.parser.parse_args()
        if args.build:
            return self._build()
        elif args.clean:
            return self._clean()
        else:
            self.parser.print_help()
            return 1
