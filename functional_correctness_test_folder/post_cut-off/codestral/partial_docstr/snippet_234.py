
import argparse
from argparse import ArgumentParser
from typing import Callable, Dict, Any
import subprocess
import os
import shutil


class Build:

    def __init__(self) -> None:
        self.parser = self._set_up_parser()

    def _set_up_parser(self) -> ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = argparse.ArgumentParser(
            description='Build and clean project.')
        parser.add_argument('--build', action='store_true',
                            help='Build the project')
        parser.add_argument('--clean', action='store_true',
                            help='Clean the project')
        parser.add_argument('--venv', action='store_true',
                            help='Set up virtual environment')
        return parser

    def _run_command(self, cmd: str, method: Callable[[str], None] = None, **kwargs: Dict[str, Any]) -> int:
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
        stdout, stderr = process.communicate()
        if method:
            method(stdout.decode('utf-8'))
        return process.returncode

    def _set_up_venv(self) -> int:
        venv_path = os.path.join(os.getcwd(), 'venv')
        if not os.path.exists(venv_path):
            return self._run_command(f'python -m venv {venv_path}')
        return 0

    def _build(self) -> int:
        return self._run_command('python setup.py build')

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        build_dirs = ['build', 'dist', 'venv']
        for dir in build_dirs:
            if os.path.exists(dir):
                shutil.rmtree(dir)
        return 0

    def main(self) -> int:
        args = self.parser.parse_args()
        if args.build:
            return self._build()
        elif args.clean:
            return self._clean()
        elif args.venv:
            return self._set_up_venv()
        else:
            self.parser.print_help()
            return 1
