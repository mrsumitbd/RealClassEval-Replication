
import argparse
from argparse import ArgumentParser
from typing import Callable, Dict, Any
import subprocess
import shutil
import os


class Build:

    def __init__(self) -> None:
        self.parser = self._set_up_parser()
        self.args = self.parser.parse_args()

    def _set_up_parser(self) -> ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = argparse.ArgumentParser(description='Build script')
        parser.add_argument('--clean', action='store_true',
                            help='Clean build directories')
        parser.add_argument('--venv', action='store_true',
                            help='Set up virtual environment')
        parser.add_argument('--build', action='store_true',
                            help='Build the project')
        return parser

    def _run_command(self, cmd: str, method: Callable[[str], None] = None, **kwargs: Dict[str, Any]) -> int:
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
        output, error = process.communicate()
        if method:
            method(output.decode('utf-8'))
        return process.returncode

    def _set_up_venv(self) -> int:
        if not os.path.exists('venv'):
            return self._run_command('python -m venv venv')
        return 0

    def _build(self) -> int:
        return self._run_command('python setup.py build')

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        build_dirs = ['build', 'dist']
        for dir in build_dirs:
            if os.path.exists(dir):
                shutil.rmtree(dir)
        return 0

    def main(self) -> int:
        if self.args.clean:
            return self._clean()
        if self.args.venv:
            return self._set_up_venv()
        if self.args.build:
            return self._build()
        self.parser.print_help()
        return 1


if __name__ == "__main__":
    build = Build()
    exit(build.main())
