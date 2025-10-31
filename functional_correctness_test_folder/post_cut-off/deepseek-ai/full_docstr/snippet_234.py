
import argparse
import os
import subprocess
import sys
import venv
from typing import Any, Callable, Dict, Optional


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
        parser = argparse.ArgumentParser(description='Build tool')
        parser.add_argument('--clean', action='store_true',
                            help='Clean build directories')
        parser.add_argument('--venv', action='store_true',
                            help='Set up virtual environment')
        parser.add_argument('--build', action='store_true',
                            help='Build from spec file')
        return parser

    def _run_command(self, cmd: str, method: Optional[Callable[[str], None]] = None, **kwargs: Dict[str, Any]) -> int:
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
            method(f'Running command: {cmd}')
        process = subprocess.Popen(cmd, shell=True, **kwargs)
        return process.wait()

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        venv_dir = 'venv'
        if not os.path.exists(venv_dir):
            venv.create(venv_dir, with_pip=True)
            return 0
        return 1

    def _build(self) -> int:
        '''
        Build from a spec file
        :return: Return code
        :rtype: int
        '''
        cmd = 'pyinstaller --onefile --noconsole spec_file.spec'
        return self._run_command(cmd, print)

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        build_dirs = ['build', 'dist']
        for dir_name in build_dirs:
            if os.path.exists(dir_name):
                import shutil
                shutil.rmtree(dir_name)
        return 0

    def main(self) -> int:
        '''
        Build
        :return: Return code
        :rtype: int
        '''
        args = self.parser.parse_args()
        if args.clean:
            return self._clean()
        if args.venv:
            return self._set_up_venv()
        if args.build:
            return self._build()
        return 0
