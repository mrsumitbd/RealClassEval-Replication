from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from glob import glob
from pathlib import Path
from typing import Any, Callable, Dict, Optional


class Build:
    def __init__(self) -> None:
        self.root_dir = Path.cwd()
        self.venv_dir = self.root_dir / ".venv"
        self.parser = self._set_up_parser()

    def _set_up_parser(self) -> ArgumentParser:
        parser = ArgumentParser(description="Build helper")
        parser.add_argument("-v", "--verbose",
                            action="store_true", help="Enable verbose output")
        subparsers = parser.add_subparsers(dest="command")

        subparsers.add_parser(
            "venv", help="Create or update virtual environment")
        subparsers.add_parser("build", help="Build the project (PEP 517/518)")
        subparsers.add_parser("clean", help="Clean build artifacts")
        subparsers.add_parser("all", help="Clean, set up venv, and build")

        parser.set_defaults(command="build")
        return parser

    def _run_command(self, cmd: str, method: Callable[[str], None] = None, **kwargs: Dict[str, Any]) -> int:
        if method is None:
            def method(line: str) -> None:
                print(line, end="")

        shell = kwargs.pop("shell", False)
        env = kwargs.pop("env", None)

        if not shell:
            args = shlex.split(cmd)
        else:
            args = cmd

        proc = subprocess.Popen(
            args,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            cwd=kwargs.pop("cwd", None),
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            method(line)
        proc.wait()
        return int(proc.returncode or 0)

    def _venv_python(self) -> Path:
        if os.name == "nt":
            return self.venv_dir / "Scripts" / "python.exe"
        return self.venv_dir / "bin" / "python"

    def _ensure_venv_exists(self) -> int:
        if self.venv_dir.exists() and self._venv_python().exists():
            return 0
        cmd = f"{shlex.quote(sys.executable)} -m venv {shlex.quote(str(self.venv_dir))}"
        return self._run_command(cmd)

    def _set_up_venv(self) -> int:
        rc = self._ensure_venv_exists()
        if rc != 0:
            return rc
        py = shlex.quote(str(self._venv_python()))
        rc = self._run_command(f"{py} -m pip install --upgrade pip")
        if rc != 0:
            return rc
        # Ensure 'build' is available
        rc = self._run_command(f"{py} -m pip install --upgrade build")
        return rc

    def _build(self) -> int:
        # Prefer venv python if available, otherwise system python
        py_exe = self._venv_python() if self._venv_python().exists() else Path(sys.executable)
        py = shlex.quote(str(py_exe))

        # Ensure build tool available
        rc = self._run_command(f"{py} -m pip install --upgrade build")
        if rc != 0:
            return rc

        return self._run_command(f"{py} -m build")

    def _clean(self) -> int:
        patterns = [
            "build",
            "dist",
            "*.egg-info",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            ".tox",
            ".coverage",
            "htmlcov",
            ".nox",
        ]

        def remove_path(p: Path) -> None:
            try:
                if p.is_dir():
                    shutil.rmtree(p, ignore_errors=True)
                elif p.exists():
                    p.unlink(missing_ok=True)
            except Exception:
                pass

        for pattern in patterns:
            # glob both in root and recursively for egg-info-like
            for match in glob(pattern):
                remove_path(Path(match))
            for match in self.root_dir.rglob(pattern):
                remove_path(match)

        return 0

    def main(self) -> int:
        args: Namespace = self.parser.parse_args()
        if args.command == "venv":
            return self._set_up_venv()
        if args.command == "clean":
            return self._clean()
        if args.command == "all":
            rc = self._clean()
            if rc != 0:
                return rc
            rc = self._set_up_venv()
            if rc != 0:
                return rc
            return self._build()
        # default: build
        # Try to ensure venv but do not fail build if venv setup fails; still attempt build
        self._set_up_venv()
        return self._build()
