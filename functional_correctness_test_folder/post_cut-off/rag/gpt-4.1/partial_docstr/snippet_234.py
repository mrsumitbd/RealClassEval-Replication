import os
import shutil
import subprocess
import sys
from argparse import ArgumentParser
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

    def _set_up_parser(self) -> ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = ArgumentParser(description="Build utility")
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
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs)
        while True:
            line = process.stdout.readline()
            if not line:
                break
            method(line.decode(errors='replace').rstrip())
        process.wait()
        return process.returncode

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        venv_dir = 'venv'
        if os.path.exists(venv_dir):
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
        if not os.path.exists('pyproject.toml') and not os.path.exists('setup.py'):
            print("No pyproject.toml or setup.py found.")
            return 1
        if os.path.exists('pyproject.toml'):
            cmd = f"{sys.executable} -m build"
        else:
            cmd = f"{sys.executable} setup.py sdist bdist_wheel"
        return self._run_command(cmd)

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        dirs = ['build', 'dist', '*.egg-info', '__pycache__']
        ret = 0
        for d in dirs:
            if '*' in d:
                for entry in os.listdir('.'):
                    if entry.endswith(d.replace('*', '')):
                        try:
                            if os.path.isdir(entry):
                                shutil.rmtree(entry)
                            else:
                                os.remove(entry)
                        except Exception as e:
                            print(f"Failed to remove {entry}: {e}")
                            ret = 1
            else:
                if os.path.exists(d):
                    try:
                        if os.path.isdir(d):
                            shutil.rmtree(d)
                        else:
                            os.remove(d)
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
