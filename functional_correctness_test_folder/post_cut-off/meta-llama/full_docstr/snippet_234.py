
import argparse
from argparse import ArgumentParser
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

    def _set_up_parser(self) -> ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = argparse.ArgumentParser(description='Build')
        subparsers = parser.add_subparsers(dest='command')

        build_parser = subparsers.add_parser('build')
        build_parser.add_argument('--spec', required=True, help='spec file')

        clean_parser = subparsers.add_parser('clean')

        venv_parser = subparsers.add_parser('venv')

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
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            if method:
                method(line.strip())
        process.wait()
        return process.returncode

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        if not os.path.exists('venv'):
            return self._run_command('python -m venv venv')
        return 0

    def _build(self, spec: str) -> int:
        '''
        Build from a spec file
        :return: Return code
        :rtype: int
        '''
        if not os.path.exists('venv'):
            print('Virtual environment not set up. Please run `build venv` first.')
            return 1
        return self._run_command(f'venv/bin/python -m build {spec}')

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
        return 0

    def main(self) -> int:
        '''
        Build
        :return: Return code
        :rtype: int
        '''
        args = self.parser.parse_args()
        if args.command == 'build':
            return self._build(args.spec)
        elif args.command == 'clean':
            return self._clean()
        elif args.command == 'venv':
            return self._set_up_venv()
        else:
            self.parser.print_help()
            return 1


if __name__ == '__main__':
    build = Build()
    exit(build.main())
