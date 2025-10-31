
import argparse
from typing import Callable, Dict, Any
import subprocess
import sys
import shutil
import os


class Build:
    """
    Build class
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        pass

    def _set_up_parser(self) -> argparse.ArgumentParser:
        """
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        """
        parser = argparse.ArgumentParser(description='Build tool')
        return parser

    def _run_command(self, cmd: str, method: Callable[[str], None] = None, **kwargs: Dict[str, Any]) -> int:
        """
        Run a command
        :param cmd: Command to run
        :type cmd: str
        :param method: Logger method
        :type method: Callable[[str], None]
        :param kwargs: Keyword arguments to pass to run_command
        :type kwargs: Dict[str, Any]
        :return: Command output
        :rtype: str
        """
        if method:
            method(f"Running command: {cmd}")
        result = subprocess.run(cmd, shell=True, **kwargs)
        return result.returncode

    def _set_up_venv(self) -> int:
        """
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        """
        venv_dir = "venv"
        if os.path.exists(venv_dir):
            shutil.rmtree(venv_dir)
        return self._run_command(f"python -m venv {venv_dir}")

    def _build(self) -> int:
        """
        Build from a spec file
        :return: Return code
        :rtype: int
        """
        return self._run_command("python -m build")

    def _clean(self) -> int:
        """
        Delete build directories
        :return: Return code
        :rtype: int
        """
        build_dirs = ["build", "dist"]
        for dir_name in build_dirs:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
        return 0

    def main(self) -> int:
        """
        Build
        :return: Return code
        :rtype: int
        """
        parser = self._set_up_parser()
        args = parser.parse_args()

        if (ret := self._clean()) != 0:
            return ret

        if (ret := self._set_up_venv()) != 0:
            return ret

        if (ret := self._build()) != 0:
            return ret

        return 0
