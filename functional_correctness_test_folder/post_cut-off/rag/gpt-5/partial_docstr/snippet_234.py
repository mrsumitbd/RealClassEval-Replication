from typing import Any, Dict, Callable, Optional
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import argparse
import subprocess
import shlex
import logging
import sys
import os
import shutil
from pathlib import Path
import glob


class Build:
    '''
    Build class
    '''

    def __init__(self) -> None:
        '''
        Constructor
        '''
        self.logger = logging.getLogger(self.__class__.__name__)
        if not logging.getLogger().handlers:
            logging.basicConfig(level=logging.INFO,
                                format='[%(levelname)s] %(message)s')
        self.parser = self._set_up_parser()
        self.args: Optional[argparse.Namespace] = None

    def _set_up_parser(self) -> ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = ArgumentParser(
            prog='build',
            description='Build utilities',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers(dest='command', metavar='COMMAND')

        p_build = subparsers.add_parser(
            'build', help='Build from a spec file', formatter_class=ArgumentDefaultsHelpFormatter)
        p_build.add_argument('--spec', type=str, default=None,
                             help='Path to the PyInstaller spec file')

        p_clean = subparsers.add_parser(
            'clean', help='Delete build directories', formatter_class=ArgumentDefaultsHelpFormatter)

        p_venv = subparsers.add_parser(
            'venv', help='Set up a Python virtual environment', formatter_class=ArgumentDefaultsHelpFormatter)
        p_venv.add_argument('--path', dest='venv_path', type=str,
                            default='.venv', help='Virtual environment directory')
        p_venv.add_argument('--requirements', dest='requirements', type=str,
                            default='requirements.txt', help='Requirements file to install')

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
        log = method or self.logger.info
        shell = bool(kwargs.pop('shell', False))
        cwd = kwargs.pop('cwd', None)
        env = kwargs.pop('env', None)

        try:
            popen_cmd = cmd if shell else shlex.split(cmd)
            with subprocess.Popen(
                popen_cmd,
                shell=shell,
                cwd=cwd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            ) as proc:
                if proc.stdout is not None:
                    for line in proc.stdout:
                        if line:
                            log(line.rstrip())
                proc.wait()
                return int(proc.returncode or 0)
        except FileNotFoundError as e:
            self.logger.error(f'Command not found: {cmd} ({e})')
            return 127
        except Exception as e:
            self.logger.error(f'Error running command: {cmd} ({e})')
            return 1

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        args = self.args or argparse.Namespace()
        venv_path_str = getattr(args, 'venv_path', '.venv')
        requirements = getattr(args, 'requirements', 'requirements.txt')
        venv_path = Path(venv_path_str)

        if venv_path.exists():
            self.logger.info(
                f'Virtual environment already exists: {venv_path}')
        else:
            self.logger.info(f'Creating virtual environment at: {venv_path}')
            rc = self._run_command(f'"{sys.executable}" -m venv "{venv_path}"')
            if rc != 0:
                return rc

        pip_exe = venv_path / ('Scripts' if os.name == 'nt' else 'bin') / \
            ('pip.exe' if os.name == 'nt' else 'pip')
        if not pip_exe.exists():
            self.logger.warning(
                f'pip not found in virtual environment: {pip_exe}')
            return 0

        rc = self._run_command(f'"{pip_exe}" install --upgrade pip')
        if rc != 0:
            return rc

        req_file = Path(requirements)
        if req_file.is_file():
            self.logger.info(f'Installing requirements from {req_file}')
            rc = self._run_command(f'"{pip_exe}" install -r "{req_file}"')
            if rc != 0:
                return rc
        else:
            self.logger.info(
                f'Requirements file not found, skipping: {req_file}')

        return 0

    def _build(self) -> int:
        '''
        Build from a spec file
        :return: Return code
        :rtype: int
        '''
        args = self.args or argparse.Namespace()
        spec: Optional[str] = getattr(args, 'spec', None)

        if not spec:
            specs = glob.glob('*.spec')
            if not specs:
                self.logger.error(
                    'No spec file provided and none found in current directory.')
                return 2
            spec = specs[0]
            self.logger.info(f'Using spec file: {spec}')

        spec_path = Path(spec)
        if not spec_path.is_file():
            self.logger.error(f'Spec file not found: {spec_path}')
            return 2

        self.logger.info(f'Building with PyInstaller spec: {spec_path}')
        cmd = f'"{sys.executable}" -m PyInstaller "{spec_path}"'
        return self._run_command(cmd)

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        rc = 0
        to_remove = [Path('build'), Path('dist')]
        for p in to_remove:
            try:
                if p.exists():
                    self.logger.info(f'Removing {p}')
                    shutil.rmtree(p)
            except Exception as e:
                self.logger.error(f'Failed to remove {p}: {e}')
                rc = 1

        # Remove __pycache__ directories recursively
        try:
            for root, dirs, _files in os.walk('.', topdown=False):
                for d in dirs:
                    if d == '__pycache__':
                        cache_dir = Path(root) / d
                        if cache_dir.exists():
                            self.logger.info(f'Removing {cache_dir}')
                            shutil.rmtree(cache_dir, ignore_errors=True)
        except Exception as e:
            self.logger.error(f'Failed to clean __pycache__: {e}')
            rc = 1

        return rc

    def main(self) -> int:
        '''
        Build
        :return: Return code
        :rtype: int
        '''
        self.args = self.parser.parse_args()
        cmd = getattr(self.args, 'command', None) if self.args else None

        if not cmd:
            # Default action: build
            self.args.command = 'build'
            cmd = 'build'

        if cmd == 'venv':
            return self._set_up_venv()
        if cmd == 'clean':
            return self._clean()
        if cmd == 'build':
            return self._build()

        self.logger.error(f'Unknown command: {cmd}')
        return 2
