from __future__ import annotations

import argparse
import logging
import os
import shutil
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Callable, Dict, Optional
import venv


class Build:
    '''
    Build class
    '''

    def __init__(self) -> None:
        '''
        Constructor
        '''
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        self.parser = self._set_up_parser()
        self.args: Optional[argparse.Namespace] = None

    def _set_up_parser(self) -> ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = argparse.ArgumentParser(
            prog='build', description='Build utilities')
        parser.add_argument('-s', '--spec', type=str,
                            help='Path to PyInstaller spec file')
        parser.add_argument('-e', '--venv', type=str,
                            help='Virtual environment directory to create/use (default: .venv)')
        parser.add_argument('--setup-venv', action='store_true',
                            help='Create and set up a virtual environment')
        parser.add_argument('-r', '--requirements', type=str,
                            help='Requirements file to install into the venv')
        parser.add_argument('--upgrade-pip', action='store_true',
                            help='Upgrade pip, setuptools and wheel in the venv')
        parser.add_argument('--pyinstaller-args', type=str, default='',
                            help='Additional arguments passed to PyInstaller')
        parser.add_argument('--no-install-pyinstaller', dest='install_pyinstaller',
                            action='store_false', help='Do not install/upgrade PyInstaller in the venv')
        parser.set_defaults(install_pyinstaller=True)
        parser.add_argument('-c', '--clean', action='store_true',
                            help='Delete build directories and exit')
        parser.add_argument('-v', '--verbose',
                            action='store_true', help='Enable verbose logging')
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
        :return: Command return code
        :rtype: int
        '''
        if method is None:
            method = self.logger.info

        popen_kwargs: Dict[str, Any] = dict(kwargs)
        popen_kwargs.setdefault('shell', True)
        popen_kwargs.setdefault('text', True)
        popen_kwargs.setdefault('stdout', subprocess.PIPE)
        popen_kwargs.setdefault('stderr', subprocess.STDOUT)

        try:
            process = subprocess.Popen(cmd, **popen_kwargs)
            if process.stdout is not None:
                for line in iter(process.stdout.readline, ''):
                    if not line:
                        break
                    method(line.rstrip())
            process.wait()
            return process.returncode
        except FileNotFoundError as e:
            method(f'Command not found: {e}')
            return 127
        except Exception as e:
            method(f'Error running command: {e}')
            return 1

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        assert self.args is not None
        venv_dir = Path(self.args.venv or '.venv')
        if not venv_dir.exists():
            self.logger.info(f'Creating virtual environment at {venv_dir}')
            try:
                builder = venv.EnvBuilder(with_pip=True, clear=False)
                builder.create(str(venv_dir))
            except Exception as e:
                self.logger.error(f'Failed to create virtual environment: {e}')
                return 1
        else:
            self.logger.info(
                f'Using existing virtual environment at {venv_dir}')

        pip_exe = self._exe_in_venv(venv_dir, 'pip')
        if not Path(pip_exe).exists():
            self.logger.error('pip not found in the virtual environment')
            return 1

        if self.args.upgrade_pip:
            self.logger.info('Upgrading pip, setuptools and wheel...')
            rc = self._run_command(
                f'"{pip_exe}" install --upgrade pip setuptools wheel')
            if rc != 0:
                return rc

        if getattr(self.args, 'install_pyinstaller', True):
            self.logger.info('Ensuring PyInstaller is installed...')
            rc = self._run_command(
                f'"{pip_exe}" install --upgrade pyinstaller')
            if rc != 0:
                return rc

        if self.args.requirements:
            req = Path(self.args.requirements)
            if not req.exists():
                self.logger.error(f'Requirements file not found: {req}')
                return 1
            self.logger.info(f'Installing requirements from {req}...')
            rc = self._run_command(f'"{pip_exe}" install -r "{req}"')
            if rc != 0:
                return rc

        return 0

    def _build(self) -> int:
        '''
        Build from a spec file
        :return: Return code
        :rtype: int
        '''
        assert self.args is not None
        spec_path: Optional[Path] = None
        if self.args.spec:
            spec_path = Path(self.args.spec)
        else:
            specs = list(Path.cwd().glob('*.spec'))
            spec_path = specs[0] if specs else None

        if not spec_path or not spec_path.exists():
            self.logger.error(
                'Spec file not found. Provide one with --spec or ensure a .spec file exists in the current directory.')
            return 2

        venv_dir = Path(self.args.venv or '.venv')
        pyinstaller_exe = None
        if venv_dir.exists():
            candidate = Path(self._exe_in_venv(venv_dir, 'pyinstaller'))
            if candidate.exists():
                pyinstaller_exe = str(candidate)

        if pyinstaller_exe is None:
            pyinstaller_exe = 'pyinstaller'

        self.logger.info(f'Building with spec: {spec_path}')
        extra = f' {self.args.pyinstaller-args}' if self.args.pyinstaller_args else ''
        cmd = f'"{pyinstaller_exe}" -y "{spec_path}"{extra}'
        rc = self._run_command(cmd, self.logger.info)
        return rc

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        targets = [Path('build'), Path('dist')]
        rc = 0
        for t in targets:
            if t.exists():
                self.logger.info(f'Removing {t}')
                try:
                    shutil.rmtree(t, ignore_errors=True)
                except Exception as e:
                    self.logger.error(f'Failed to remove {t}: {e}')
                    rc = 1
        # Remove egg-info directories if present
        for egg in Path.cwd().glob('*.egg-info'):
            if egg.is_dir():
                self.logger.info(f'Removing {egg}')
                try:
                    shutil.rmtree(egg, ignore_errors=True)
                except Exception as e:
                    self.logger.error(f'Failed to remove {egg}: {e}')
                    rc = 1
        return rc

    def main(self) -> int:
        '''
        Build
        :return: Return code
        :rtype: int
        '''
        self.args = self.parser.parse_args()
        if self.args.verbose:
            self.logger.setLevel(logging.DEBUG)

        if self.args.clean:
            return self._clean()

        rc = 0
        if self.args.setup_venv or self.args.venv:
            rc = self._set_up_venv()
            if rc != 0:
                return rc

        rc = self._build()
        return rc

    @staticmethod
    def _exe_in_venv(venv_dir: Path, exe_name: str) -> str:
        bin_dir = 'Scripts' if os.name == 'nt' else 'bin'
        suffix = '.exe' if os.name == 'nt' else ''
        return str(venv_dir / bin_dir / f'{exe_name}{suffix}')
