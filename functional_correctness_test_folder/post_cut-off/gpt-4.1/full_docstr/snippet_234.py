
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
        self.venv_dir = "venv"
        self.build_dir = "build"
        self.dist_dir = "dist"
        self.spec_file = "setup.py"

    def _set_up_parser(self) -> ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = argparse.ArgumentParser(description="Build utility")
        parser.add_argument(
            "command",
            choices=["venv", "build", "clean"],
            help="Action to perform: venv, build, clean"
        )
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
        method(f"Running command: {cmd}")
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                **kwargs
            )
            if result.stdout:
                method(result.stdout)
            if result.stderr:
                method(result.stderr)
            return result.returncode
        except Exception as e:
            method(f"Error running command: {e}")
            return 1

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        if os.path.exists(self.venv_dir):
            print(f"Virtual environment '{self.venv_dir}' already exists.")
            return 0
        cmd = f"{sys.executable} -m venv {self.venv_dir}"
        return self._run_command(cmd)

    def _build(self) -> int:
        '''
        Build from a spec file
        :return: Return code
        :rtype: int
        '''
        if not os.path.exists(self.spec_file):
            print(f"Spec file '{self.spec_file}' not found.")
            return 1
        # Clean previous build/dist
        self._clean()
        cmd = f"{sys.executable} {self.spec_file} sdist bdist_wheel"
        return self._run_command(cmd)

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        ret = 0
        for d in [self.build_dir, self.dist_dir, f"{self.spec_file.replace('.py', '')}.egg-info"]:
            if os.path.exists(d):
                try:
                    if os.path.isdir(d):
                        shutil.rmtree(d)
                    else:
                        os.remove(d)
                    print(f"Removed '{d}'")
                except Exception as e:
                    print(f"Failed to remove '{d}': {e}")
                    ret = 1
        return ret

    def main(self) -> int:
        '''
        Build
        :return: Return code
        :rtype: int
        '''
        args = self.parser.parse_args()
        if args.command == "venv":
            return self._set_up_venv()
        elif args.command == "build":
            return self._build()
        elif args.command == "clean":
            return self._clean()
        else:
            print("Unknown command")
            return 1
