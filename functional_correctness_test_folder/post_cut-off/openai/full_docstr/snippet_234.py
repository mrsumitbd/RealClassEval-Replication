
import argparse
import logging
import os
import shutil
import subprocess
import sys
from typing import Any, Callable, Dict, Optional


class Build:
    '''
    Build class
    '''

    def __init__(self) -> None:
        '''
        Constructor
        '''
        self.logger = logging.getLogger(self.__class__.__name__)
        self.parser = self._set_up_parser()
        self.args = self.parser.parse_args()

    def _set_up_parser(self) -> argparse.ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = argparse.ArgumentParser(description='Build helper')
        parser.add_argument(
            '--venv',
            action='store_true',
            help='Set up a virtual environment'
        )
        parser.add_argument(
            '--build',
            action='store_true',
            help='Build the package'
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Clean build artifacts'
        )
        parser.add_argument(
            '--spec',
            default='setup.py',
            help='Path to the spec file (default: setup.py)'
        )
        return parser

    def _run_command(
        self,
        cmd: str,
        method: Optional[Callable[[str], None]] = None,
        **kwargs: Dict[str, Any]
    ) -> int:
        '''
        Run a command
        :param cmd: Command to run
        :type cmd: str
        :param method: Logger method
        :type method: Callable[[str], None]
        :param kwargs: Keyword arguments to pass to run_command
        :type kwargs: Dict[str, Any]
        :return: Command return code
        :rtype: int
        '''
        if method is None:
            method = self.logger.info

        method(f'Running command: {cmd}')
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                **kwargs
            )
            method(result.stdout)
            return result.returncode
        except Exception as exc:
            self.logger.error(f'Command failed: {exc}')
            return 1

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        venv_dir = 'venv'
        if os.path.isdir(venv_dir):
            self.logger.info('Virtual environment already exists')
            return 0
        cmd = f'{sys.executable} -m venv {venv_dir}'
        return self._run_command(cmd)

    def _build(self) -> int:
        '''
        Build from a spec file
        :return: Return code
        :rtype: int
        '''
        spec_path = self.args.spec
        if not os.path.isfile(spec_path):
            self.logger.error(f'Spec file not found: {spec_path}')
            return 1

        # Ensure virtual environment exists
        venv_dir = 'venv'
        if not os.path.isdir(venv_dir):
            self.logger.info('Virtual environment not found, creating one')
            rc = self._set_up_venv()
            if rc != 0:
                return rc

        # Determine python executable inside venv
        if os.name == 'nt':
            python_bin = os.path.join(venv_dir, 'Scripts', 'python.exe')
        else:
            python_bin = os.path.join(venv_dir, 'bin', 'python')

        if not os.path.isfile(python_bin):
            self.logger.error(
                f'Python executable not found in venv: {python_bin}')
            return 1

        # Build command
        cmd = f'{python_bin} {spec_path} sdist bdist_wheel'
        return self._run_command(cmd)

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        dirs_to_remove = ['build', 'dist']
        # Remove egg-info directories
        for item in os.listdir('.'):
            if item.endswith('.egg-info') and os.path.isdir(item):
                dirs_to_remove.append(item)

        # Remove venv
        if os.path.isdir('venv'):
            dirs_to_remove.append('venv')

        rc = 0
        for d in dirs_to_remove:
            if os.path.isdir(d):
                try:
                    shutil.rmtree(d)
                    self.logger.info(f'Removed directory: {d}')
                except Exception as exc:
                    self.logger.error(f'Failed to remove {d}: {exc}')
                    rc = 1
        return rc

    def main(self) -> int:
        '''
        Build
        :return: Return code
        :rtype: int
        '''
        rc = 0
        if self.args.clean:
            rc = self._clean()
            if rc != 0:
                return rc

        if self.args.venv:
            rc = self._set_up_venv()
            if rc != 0:
                return rc

        if self.args.build:
            rc = self._build()
            if rc != 0:
                return rc

        return rc
