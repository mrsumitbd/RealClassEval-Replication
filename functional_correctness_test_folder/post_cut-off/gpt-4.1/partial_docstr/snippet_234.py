
import argparse
import os
import shutil
import subprocess
from argparse import ArgumentParser
from typing import Callable, Dict, Any


class Build:
    def __init__(self) -> None:
        self.build_dir = "build"
        self.dist_dir = "dist"
        self.venv_dir = ".venv"

    def _set_up_parser(self) -> ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = argparse.ArgumentParser(description="Build utility")
        parser.add_argument(
            "command",
            choices=["build", "clean", "venv"],
            help="Command to run: build, clean, venv"
        )
        return parser

    def _run_command(self, cmd: str, method: Callable[[str], None] = None, **kwargs: Dict[str, Any]) -> int:
        try:
            proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                **kwargs
            )
            stdout, stderr = proc.communicate()
            if method:
                if stdout:
                    method(stdout.decode())
                if stderr:
                    method(stderr.decode())
            else:
                if stdout:
                    print(stdout.decode(), end="")
                if stderr:
                    print(stderr.decode(), end="")
            return proc.returncode
        except Exception as e:
            print(f"Error running command '{cmd}': {e}")
            return 1

    def _set_up_venv(self) -> int:
        if os.path.exists(self.venv_dir):
            print(f"Virtual environment already exists at {self.venv_dir}")
            return 0
        cmd = f"python -m venv {self.venv_dir}"
        print(f"Setting up virtual environment: {cmd}")
        return self._run_command(cmd)

    def _build(self) -> int:
        # Clean previous builds
        self._clean()
        # Build using setuptools if setup.py exists, else error
        if os.path.exists("setup.py"):
            cmd = "python setup.py sdist bdist_wheel"
        elif os.path.exists("pyproject.toml"):
            cmd = "python -m build"
        else:
            print("No setup.py or pyproject.toml found for building.")
            return 1
        print(f"Building project: {cmd}")
        return self._run_command(cmd)

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        code = 0
        for d in [self.build_dir, self.dist_dir, f"{self.venv_dir}", "*.egg-info"]:
            if "*" in d:
                # Remove all matching directories
                for item in os.listdir("."):
                    if item.endswith(".egg-info") and os.path.isdir(item):
                        try:
                            shutil.rmtree(item)
                            print(f"Deleted {item}")
                        except Exception as e:
                            print(f"Failed to delete {item}: {e}")
                            code = 1
            elif os.path.exists(d):
                try:
                    shutil.rmtree(d)
                    print(f"Deleted {d}")
                except Exception as e:
                    print(f"Failed to delete {d}: {e}")
                    code = 1
        return code

    def main(self) -> int:
        parser = self._set_up_parser()
        args = parser.parse_args()
        if args.command == "build":
            return self._build()
        elif args.command == "clean":
            return self._clean()
        elif args.command == "venv":
            return self._set_up_venv()
        else:
            print(f"Unknown command: {args.command}")
            return 1
