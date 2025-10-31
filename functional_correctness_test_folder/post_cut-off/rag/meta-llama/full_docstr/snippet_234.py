
import argparse
import subprocess
from typing import Callable, Dict, Any
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
        self.logger.info(f'Running command: {cmd}')
        try:
            subprocess.check_call(cmd, shell=True, **kwargs)
            return 0
        except subprocess.CalledProcessError as e:
            if method:
                method(f'Command failed with return code {e.returncode}')
            return e.returncode

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        if not os.path.exists('venv'):
            return self._run_command('python -m venv venv')
        return 0

    def _build(self) -> int:
        '''
        Build from a spec file
        :return: Return code
        :rtype: int
        '''
        spec_file = os.environ.get('SPEC_FILE')
        if not spec_file:
            self.logger.error('SPEC_FILE environment variable not set')
            return 1

        return self._run_command(f'python -m PyInstaller --onefile {spec_file}')

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        try:
            shutil.rmtree('build')
            shutil.rmtree('dist')
        except FileNotFoundError:
            pass
        return 0

    def main(self) -> int:
        '''
        Build
        :return: Return code
        :rtype: int
        '''
        parser = self._set_up_parser()
        args = parser.parse_args()

        if args.command == 'build':
            return self._build()
        elif args.command == 'clean':
            return self._clean()
        else:
            parser.print_help()
            return 1
