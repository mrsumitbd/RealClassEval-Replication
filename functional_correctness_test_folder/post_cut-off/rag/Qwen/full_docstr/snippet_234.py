
import argparse
import subprocess
import os
import shutil
from typing import Callable, Dict, Any


class Build:
    '''
    Build class
    '''

    def __init__(self) -> None:
        '''
        Constructor
        '''
        self.parser = self._set_up_parser()
        self.args = self.parser.parse_args()

    def _set_up_parser(self) -> argparse.ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = argparse.ArgumentParser(description='Build script')
        parser.add_argument('--clean', action='store_true',
                            help='Clean build directories')
        parser.add_argument('--venv', action='store_true',
                            help='Set up a Python virtual environment')
        parser.add_argument('--build', action='store_true',
                            help='Build from a spec file')
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
        if method:
            method(f"Running command: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, check=True, **kwargs)
            return result.returncode
        except subprocess.CalledProcessError as e:
            if method:
                method(f"Command failed: {e}")
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
        return self._run_command('pyinstaller your_spec_file.spec')

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        shutil.rmtree('build', ignore_errors=True)
        shutil.rmtree('dist', ignore_errors=True)
        shutil.rmtree('venv', ignore_errors=True)
        os.remove('your_spec_file.spec') if os.path.exists(
            'your_spec_file.spec') else None
        return 0

    def main(self) -> int:
        '''
        Build
        :return: Return code
        :rtype: int
        '''
        if self.args.clean:
            return self._clean()
        if self.args.venv:
            return self._set_up_venv()
        if self.args.build:
            return self._build()
        self.parser.print_help()
        return 1
