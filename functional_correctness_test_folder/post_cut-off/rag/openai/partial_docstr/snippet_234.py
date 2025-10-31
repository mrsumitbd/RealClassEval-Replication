
import argparse
import os
import shutil
import subprocess
import sys
from argparse import ArgumentParser
from typing import Any, Callable, Dict, Optional


class Build:
    """
    Build class
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.parser = self._set_up_parser()

    def _set_up_parser(self) -> ArgumentParser:
        """
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        """
        parser = argparse.ArgumentParser(
            description="Build, clean and set up virtual environment for the project."
        )
        subparsers = parser.add_subparsers(dest="command", required=True)

        # venv command
        subparsers.add_parser(
            "venv",
            help="Set up a Python virtual environment (venv).",
        )

        # build command
        subparsers.add_parser(
            "build",
            help="Build the project from the spec file.",
        )

        # clean command
        subparsers.add_parser(
            "clean",
            help="Delete build directories.",
        )

        return parser

    def _run_command(
        self,
        cmd: str,
        method: Optional[Callable[[str], None]] = None,
        **kwargs: Dict[str, Any],
    ) -> int:
        """
        Run a command
        :param cmd: Command to run
        :type cmd: str
        :param method: Logger method
        :type method: Callable[[str], None]
        :param kwargs: Keyword arguments to pass to run_command
        :type kwargs: Dict[str, Any]
        :return: Return code
        :rtype: int
        """
        if method:
            method(f"Running command: {cmd}")
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                **kwargs,
            )
            if method:
                method(result.stdout)
            return result.returncode
        except Exception as exc:
            if method:
                method(f"Command failed: {exc}")
            return 1

    def _set_up_venv(self) -> int:
        """
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        """
        venv_dir = "venv"
        if os.path.isdir(venv_dir):
            return 0  # already exists
        return self._run_command(f"{sys.executable} -m venv {venv_dir}")

    def _build(self) -> int:
        """
        Build from a spec file
        :return: Return code
        :rtype: int
        """
        # Ensure virtual environment is activated
        venv_dir = "venv"
        if not os.path.isdir(venv_dir):
            return self._set_up_venv()

        # Install build dependencies
        pip_path = os.path.join(venv_dir, "Scripts", "pip") if os.name == "nt" else os.path.join(
            venv_dir, "bin", "pip")
        if not os.path.isfile(pip_path):
            pip_path = "pip"

        # Install build tool
        rc = self._run_command(f"{pip_path} install --upgrade build")
        if rc != 0:
            return rc

        # Run the build
        # install project locally
        return self._run_command(f"{pip_path} install .")
        # Alternatively, use PEP 517 build:
        # return self._run_command(f"{pip_path} install build && python -m build")

    def _clean(self) -> int:
        """
        Delete build directories
        :return: Return code
        :rtype: int
        """
        dirs_to_remove = ["build", "dist"]
        # Remove *.egg-info directories
        for item in os.listdir("."):
            if item.endswith(".egg-info") and os.path.isdir(item):
                dirs_to_remove.append(item)

        rc = 0
        for d in dirs_to_remove:
            if os.path.isdir(d):
                try:
                    shutil.rmtree(d)
                except Exception as exc:
                    rc = 1
        return rc

    def main(self) -> int:
        """
        Build
        :return: Return code
        :rtype: int
        """
        args = self.parser.parse_args()
        if args.command == "venv":
            return self._set_up_venv()
        elif args.command == "build":
            return self._build()
        elif args.command == "clean":
            return self._clean()
        else:
            self.parser.print_help()
            return 1
