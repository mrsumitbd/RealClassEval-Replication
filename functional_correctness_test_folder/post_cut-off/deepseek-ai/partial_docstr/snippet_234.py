
import argparse
import os
import subprocess
import sys
import venv
from typing import Any, Callable, Dict, Optional


class Build:

    def __init__(self) -> None:
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
        parser.add_argument('--no-venv', action='store_true',
                            help='Skip virtual environment setup')
        return parser

    def _run_command(self, cmd: str, method: Optional[Callable[[str], None]] = None, **kwargs: Dict[str, Any]) -> int:
        if method is None:
            method = print
        method(f"Running command: {cmd}")
        return subprocess.call(cmd, shell=True, **kwargs)

    def _set_up_venv(self) -> int:
        if not os.path.exists('venv'):
            venv.create('venv', with_pip=True)
        return 0

    def _build(self) -> int:
        return self._run_command("python -m pip install -e .")

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        build_dirs = ['build', 'dist', '*.egg-info']
        for dir_name in build_dirs:
            self._run_command(f"rm -rf {dir_name}")
        return 0

    def main(self) -> int:
        args = self.parser.parse_args()
        if args.clean:
            return self._clean()
        if not args.no_venv:
            venv_result = self._set_up_venv()
            if venv_result != 0:
                return venv_result
        return self._build()
