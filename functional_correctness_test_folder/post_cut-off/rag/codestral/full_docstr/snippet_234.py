
import argparse
from argparse import ArgumentParser
from typing import Callable, Dict, Any
import subprocess
import sys
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

    def _set_up_parser(self) -> ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = argparse.ArgumentParser(description='Build tool')
        parser.add_argument('--venv', action='store_true',
                            help='Set up a Python virtual environment')
        parser.add_argument('--build', action='store_true',
                            help='Build from a spec file')
        parser.add_argument('--clean', action='store_true',
                            help='Delete build directories')
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
        if method is None:
            method = print
        method(f'Running command: {cmd}')
        result = subprocess.run(cmd, shell=True, **kwargs)
        return result.returncode

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        if os.path.exists('venv'):
            print('Virtual environment already exists')
            return 0
        return self._run_command('python -m venv venv')

    def _build(self) -> int:
        '''
        Build from a spec file
        :return: Return code
        :rtype: int
        '''
        if not os.path.exists('spec.json'):
            print('spec.json not found')
            return 1
        return self._run_command('python -m pip install -r requirements.txt && python setup.py build')

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('venv'):
            shutil.rmtree('venv')
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
        elif args.build:
            return self._build()
        elif args.clean:
            return self._clean()
        else:
            self.parser.print_help()
            return 1


if __name__ == '__main__':
    build = Build()
    sys.exit(build.main())
