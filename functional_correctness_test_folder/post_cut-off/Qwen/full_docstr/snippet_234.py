
import argparse
from typing import Callable, Dict, Any
import subprocess
import os
import shutil


class Build:
    '''
    Build class
    '''

    def __init__(self) -> None:
        '''
        Constructor
        '''
        self.parser = self._set_up_parser()

    def _set_up_parser(self) -> argparse.ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = argparse.ArgumentParser(description='Build script')
        parser.add_argument('--build', action='store_true',
                            help='Build the project')
        parser.add_argument('--clean', action='store_true',
                            help='Clean build directories')
        parser.add_argument('--venv', action='store_true',
                            help='Set up a virtual environment')
        return parser

    def _run_command(self, cmd: str, method: Callable[[str], None] = None, **kwargs: Dict[str, Any]) -> int:
        '''
        Run a command
        :param cmd: Command to run
        :type cmd: str
        :param method: Logger method
        :type method: Callable[[str], None]
        :param kwargs: Keyword arguments to pass to run_command
        :type kwargs: Dict[str, Any]
        :return: Command output
        :rtype: str
        '''
        try:
            result = subprocess.run(cmd, shell=True, check=True, **kwargs)
            if method:
                method(f"Command succeeded: {cmd}")
            return result.returncode
        except subprocess.CalledProcessError as e:
            if method:
                method(f"Command failed: {cmd}")
            return e.returncode

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        return self._run_command('python -m venv venv')

    def _build(self) -> int:
        '''
        Build from a spec file
        :return: Return code
        :rtype: int
        '''
        return self._run_command('python setup.py build')

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        shutil.rmtree('build', ignore_errors=True)
        shutil.rmtree('dist', ignore_errors=True)
        shutil.rmtree('venv', ignore_errors=True)
        return 0

    def main(self) -> int:
        '''
        Build
        :return: Return code
        :rtype: int
        '''
        args = self.parser.parse_args()
        if args.venv:
            return self._set_up_venv()
        if args.build:
            return self._build()
        if args.clean:
            return self._clean()
        return 1
