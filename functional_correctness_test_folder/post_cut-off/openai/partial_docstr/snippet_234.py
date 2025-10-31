
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Dict, Optional


class Build:
    """
    Simple build helper for Python projects.
    """

    def __init__(self) -> None:
        self.parser = self._set_up_parser()
        self.args = self.parser.parse_args()

    def _set_up_parser(self) -> argparse.ArgumentParser:
        """
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        """
        parser = argparse.ArgumentParser(
            description="Build helper for Python projects."
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "--clean",
            action="store_true",
            help="Clean build artifacts.",
        )
        group.add_argument(
            "--build",
            action="store_true",
            help="Build distribution packages.",
        )
        group.add_argument(
            "--venv",
            action="store_true",
            help="Set up virtual environment.",
        )
        group.add_argument(
            "--all",
            action="store_true",
            help="Run all steps: venv, clean, build.",
        )
        return parser

    def _run_command(
        self,
        cmd: str,
        method: Optional[Callable[[str], None]] = None,
        **kwargs: Dict[str, Any],
    ) -> int:
        """
        Execute a shell command.
        :param cmd: Command string.
        :param method: Optional callback to process output.
        :param kwargs: Additional kwargs for subprocess.run.
        :return: Return code.
        """
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=False,
                capture_output=True,
                text=True,
                **kwargs,
            )
            if method:
                method(result.stdout)
            if result.stderr:
                sys.stderr.write(result.stderr)
            return result.returncode
        except Exception as exc:
            sys.stderr.write(f"Error running command '{cmd}': {exc}\n")
            return 1

    def _set_up_venv(self) -> int:
        """
        Create a virtual environment and install dependencies.
        :return: Return code.
        """
        venv_path = Path("venv")
        if venv_path.exists():
            print("Virtual environment already exists.")
        else:
            print("Creating virtual environment...")
            ret = self._run_command(f"{sys.executable} -m venv {venv_path}")
            if ret != 0:
                return ret

        pip_path = venv_path / ("Scripts" if os.name ==
                                "nt" else "bin") / "pip"
        req_file = Path("requirements.txt")
        if req_file.exists():
            print("Installing dependencies...")
            ret = self._run_command(f"{pip_path} install -r {req_file}")
            if ret != 0:
                return ret
        else:
            print("No requirements.txt found; skipping dependency installation.")
        return 0

    def _build(self) -> int:
        """
        Build source and wheel distributions.
        :return: Return code.
        """
        print("Building distributions...")
        # Prefer the 'build' module if available
        try:
            import build  # noqa: F401
            ret = self._run_command(f"{sys.executable} -m build")
        except ImportError:
            # Fallback to setup.py
            ret = self._run_command(
                f"{sys.executable} setup.py sdist bdist_wheel")
        return ret

    def _clean(self) -> int:
        """
        Delete build directories.
        :return: Return code.
        """
        dirs_to_remove = ["build", "dist"]
        # Remove *.egg-info directories
        for path in Path(".").glob("*.egg-info"):
            dirs_to_remove.append(str(path))

        for d in dirs_to_remove:
            dir_path = Path(d)
            if dir_path.exists():
                print(f"Removing {dir_path}...")
                try:
                    shutil.rmtree(dir_path)
                except Exception as exc:
                    sys.stderr.write(f"Failed to remove {dir_path}: {exc}\n")
                    return 1
        return 0

    def main(self) -> int:
        """
        Main entry point.
        """
        if self.args.clean:
            return self._clean()
        if self.args.build:
            return self._build()
        if self.args.venv:
            return self._set_up_venv()
        if self.args.all:
            ret = self._set_up_venv()
            if ret != 0:
                return ret
            ret = self._clean()
            if ret != 0:
                return ret
            return self._build()
        # If no arguments, show help
        self.parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(Build().main())
