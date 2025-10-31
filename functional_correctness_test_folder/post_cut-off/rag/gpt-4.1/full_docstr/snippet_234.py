
import argparse
import subprocess
import sys
import os
import shutil
from typing import Callable, Dict, Any
from argparse import ArgumentParser


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
        parser = argparse.ArgumentParser(description="Build utility")
        parser.add_argument('command', choices=[
                            'build', 'clean', 'venv'], help='Command to run')
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
        if method is None:
            method = print
        try:
            process = subprocess.Popen(
                cmd, shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                **kwargs
            )
            for line in process.stdout:
                method(line.rstrip())
            process.wait()
            return process.returncode
        except Exception as e:
            method(f"Error running command '{cmd}': {e}")
            return 1

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        venv_dir = 'venv'
        if os.path.isdir(venv_dir):
            print("Virtual environment already exists.")
            return 0
        cmd = f"{sys.executable} -m venv {venv_dir}"
        return self._run_command(cmd)

    def _build(self) -> int:
        '''
        Build from a spec file
        :return: Return code
        :rtype: int
        '''
        # Example: build using setup.py or pyproject.toml
        if os.path.exists('pyproject.toml'):
            cmd = f"{sys.executable} -m build"
        elif os.path.exists('setup.py'):
            cmd = f"{sys.executable} setup.py sdist bdist_wheel"
        else:
            print("No build specification file found (pyproject.toml or setup.py).")
            return 1
        return self._run_command(cmd)

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        dirs = ['build', 'dist', '*.egg-info', 'venv']
        ret = 0
        for d in dirs:
            if '*' in d:
                import glob
                for path in glob.glob(d):
                    if os.path.isdir(path):
                        try:
                            shutil.rmtree(path)
                            print(f"Removed directory: {path}")
                        except Exception as e:
                            print(f"Failed to remove {path}: {e}")
                            ret = 1
            elif os.path.isdir(d):
                try:
                    shutil.rmtree(d)
                    print(f"Removed directory: {d}")
                except Exception as e:
                    print(f"Failed to remove {d}: {e}")
                    ret = 1
        return ret

    def main(self) -> int:
        '''
        Build
        :return: Return code
        :rtype: int
        '''
        args = self.parser.parse_args()
        if args.command == 'build':
            return self._build()
        elif args.command == 'clean':
            return self._clean()
        elif args.command == 'venv':
            return self._set_up_venv()
        else:
            print(f"Unknown command: {args.command}")
            return 1
