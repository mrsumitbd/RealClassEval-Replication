
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
            description="Build helper: set up venv, build package, clean build artefacts."
        )
        sub = parser.add_subparsers(dest="command", required=True)

        sub.add_parser("venv", help="Create a Python virtual environment.")
        sub.add_parser(
            "build", help="Build the package from the current directory.")
        sub.add_parser("clean", help="Remove build artefacts.")
        sub.add_parser("all", help="Run venv, build and clean in sequence.")

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
        if method is None:
            method = print

        method(f"Running: {cmd}")
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
            method(result.stdout)
            return result.returncode
        except Exception as exc:
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
            print(f"Virtual environment already exists at {venv_dir}")
            return 0

        cmd = f"{sys.executable} -m venv {venv_dir}"
        return self._run_command(cmd)

    def _build(self) -> int:
        """
        Build from a spec file
        :return: Return code
        :rtype: int
        """
        # Use the standard build module if available
        cmd = f"{sys.executable} -m build"
        return self._run_command(cmd)

    def _clean(self) -> int:
        """
        Delete build directories
        :return: Return code
        :rtype: int
        """
        dirs_to_remove = ["build", "dist"]
        # Remove *.egg-info directories
        egg_info_dirs = [
            d for d in os.listdir(".") if d.endswith(".egg-info") and os.path.isdir(d)
        ]
        dirs_to_remove.extend(egg_info_dirs)

        rc = 0
        for d in dirs_to_remove:
            if os.path.isdir(d):
                try:
                    shutil.rmtree(d)
                    print(f"Removed {d}")
                except Exception as exc:
                    print(f"Failed to remove {d}: {exc}")
                    rc = 1
        return rc

    def main(self) -> int:
        """
        Build
        :return: Return code
        :rtype: int
        """
        args = self.parser.parse_args()
        cmd = args.command

        if cmd == "venv":
            return self._set_up_venv()
        if cmd == "build":
            return self._build()
        if cmd == "clean":
            return self._clean()
        if cmd == "all":
            rc = self._set_up_venv()
            if rc != 0:
                return rc
            rc = self._build()
            if rc != 0:
                return rc
            return self._clean()

        # Should never reach here
        return 1
