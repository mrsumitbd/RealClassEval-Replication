
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
        parser = argparse.ArgumentParser(description='Build a Python project')
        parser.add_argument('--spec', type=str, help='Path to the spec file')
        parser.add_argument('--clean', action='store_true',
                            help='Clean build directories')
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
        process = subprocess.Popen(cmd, shell=True, **kwargs)
        process.wait()
        return process.returncode

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        venv_dir = 'venv'
        if not os.path.exists(venv_dir):
            return self._run_command(f'python -m venv {venv_dir}')
        return 0

    def _build(self) -> int:
        '''
        Build from a spec file
        :return: Return code
        :rtype: int
        '''
        spec_file = self.parser.parse_args().spec
        if not spec_file:
            print("Error: Spec file not provided")
            return 1

        with open(spec_file, 'r') as f:
            spec = f.read()

        # Parse spec file and build project
        # This is a placeholder for the actual implementation
        print("Building project from spec file...")
        return 0

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        venv_dir = 'venv'
        if os.path.exists(venv_dir):
            shutil.rmtree(venv_dir)
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
        else:
            ret = self._set_up_venv()
            if ret != 0:
                return ret
            return self._build()
