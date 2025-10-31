
import argparse
from argparse import ArgumentParser
from typing import Callable, Dict, Any
import subprocess
import sys


class Build:

    def __init__(self) -> None:
        self.parser = self._set_up_parser()

    def _set_up_parser(self) -> ArgumentParser:
        parser = argparse.ArgumentParser(description='Build script')
        subparsers = parser.add_subparsers(dest='command')

        subparsers.add_parser('build', help='Build the project')
        subparsers.add_parser('clean', help='Clean the project')
        subparsers.add_parser('venv', help='Set up the virtual environment')

        return parser

    def _run_command(self, cmd: str, method: Callable[[str], None] = None, **kwargs: Dict[str, Any]) -> int:
        try:
            if method:
                method(cmd, **kwargs)
            else:
                subprocess.check_call(cmd, shell=True)
            return 0
        except subprocess.CalledProcessError as e:
            return e.returncode

    def _set_up_venv(self) -> int:
        return self._run_command('python -m venv venv')

    def _build(self) -> int:
        return self._run_command('python -m pip install -r requirements.txt')

    def _clean(self) -> int:
        return self._run_command('rm -rf build dist *.egg-info', shell=True)

    def main(self) -> int:
        args = self.parser.parse_args()

        if args.command == 'build':
            return self._build()
        elif args.command == 'clean':
            return self._clean()
        elif args.command == 'venv':
            return self._set_up_venv()
        else:
            self.parser.print_help()
            return 1


if __name__ == '__main__':
    sys.exit(Build().main())
