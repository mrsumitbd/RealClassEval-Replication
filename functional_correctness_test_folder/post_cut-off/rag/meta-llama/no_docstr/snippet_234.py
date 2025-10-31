
import argparse
from typing import Callable, Dict, Any
import subprocess
import logging
import shutil
import os


class Build:
    '''
    Build class
    '''

    def __init__(self) -> None:
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)

    def _set_up_parser(self) -> argparse.ArgumentParser:
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
        :rtype: int
        '''
        try:
            output = subprocess.check_output(cmd, shell=True, **kwargs)
            if method:
                method(output.decode('utf-8').strip())
            return 0
        except subprocess.CalledProcessError as e:
            if method:
                method(e.output.decode('utf-8').strip(), exc_info=True)
            return e.returncode

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        if not os.path.exists('venv'):
            return self._run_command('python -m venv venv', self.logger.info)
        return 0

    def _build(self, spec: str) -> int:
        '''
        Build from a spec file
        :return: Return code
        :rtype: int
        '''
        return self._run_command(f'python -m build --spec {spec}', self.logger.info)

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        try:
            shutil.rmtree('build')
            return 0
        except FileNotFoundError:
            self.logger.warning('Build directory not found')
            return 0
        except Exception as e:
            self.logger.error('Failed to clean build directory', exc_info=True)
            return 1

    def main(self) -> int:
        '''
        Build
        :return: Return code
        :rtype: int
        '''
        parser = self._set_up_parser()
        args = parser.parse_args()

        if args.command == 'build':
            return self._build(args.spec)
        elif args.command == 'clean':
            return self._clean()
        else:
            parser.print_help()
            return 1
