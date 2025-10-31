
import argparse
import os
import shutil
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Callable, Dict, Optional


class Build:
    """
    Build class
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.project_root = Path(__file__).resolve().parent
        self.venv_dir = self.project_root / "venv"

    def _set_up_parser(self) -> ArgumentParser:
        """
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        """
        parser = argparse.ArgumentParser(
            description="Build, clean, and set up virtual environment for the project."
        )
        sub = parser.add_subparsers(dest="command", required=True)

        sub.add_parser("venv", help="Set up a Python virtual environment.")
        sub.add_parser("build", help="Build the project from the spec file.")
        sub.add_parser("clean", help="Delete build directories.")
        sub.add_parser("all", help="Run venv, build, and clean in sequence.")

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
        :return: Command output
        :rtype: str
        """
        if method is None:
            method = print

        method(f"Running: {cmd}")
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=self.project_root,
            capture_output=True,
            text=True,
            **kwargs,
        )
        if result.stdout:
            method(result.stdout.strip())
        if result.stderr:
            method(result.stderr.strip())
        return result.returncode

    def _set_up_venv(self) -> int:
        """
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        """
        if self.venv_dir.exists():
            print(f"Virtual environment already exists at {self.venv_dir}")
            return 0
        cmd = f"{sys.executable} -m venv {self.venv_dir}"
        return self._run_command(cmd)

    def _build(self) -> int:
        """
        Build from a spec file
        :return: Return code
        :rtype: int
        """
        # Use pip to install the package in editable mode
        cmd = f"{self.venv_dir / 'bin' / 'pip'} install -e ."
        return self._run_command(cmd)

    def _clean(self) -> int:
        """
        Delete build directories
        :return: Return code
        :rtype: int
        """
        dirs_to_remove = [
            self.project_root / "build",
            self.project_root / "dist",
            self.project_root / "venv",
        ]

        # Remove *.egg-info directories
        for p in self.project_root.glob("*.egg-info"):
            dirs_to_remove.append(p)

        for d in dirs_to_remove:
            if d.exists():
                try:
                    shutil.rmtree(d)
                    print(f"Removed {d}")
                except Exception as e:
                    print(f"Failed to remove {d}: {e}")
                    return 1
        return 0

    def main(self) -> int:
        """
        Build
        :return: Return code
        :rtype: int
        """
        parser = self._set_up_parser()
        args = parser.parse_args()

        if args.command == "venv":
            return self._set_up_venv()
        elif args.command == "build":
            return self._build()
        elif args.command == "clean":
            return self._clean()
        elif args.command == "all":
            rc = self._set_up_venv()
            if rc != 0:
                return rc
            rc = self._build()
            if rc != 0:
                return rc
            rc = self._clean()
            return rc
        else:
            parser.print_help()
            return 1


if __name__ == "__main__":
    sys.exit(Build().main())
