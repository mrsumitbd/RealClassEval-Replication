from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, Callable, Dict, Optional


class Build:
    def __init__(self) -> None:
        self.root_dir: Path = Path.cwd()
        self.venv_dir: Path = self.root_dir / ".venv"
        self.parser: ArgumentParser = self._set_up_parser()
        self.args: Optional[Namespace] = None

    def _set_up_parser(self) -> ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = argparse.ArgumentParser(
            prog="build", description="Project build utility")
        parser.add_argument("-v", "--verbose", action="count",
                            default=0, help="Increase output verbosity")
        parser.add_argument("-q", "--quiet", action="store_true",
                            help="Suppress non-error output")

        subparsers = parser.add_subparsers(dest="command")

        # venv command
        p_venv = subparsers.add_parser(
            "venv", help="Create and prepare virtual environment")
        p_venv.add_argument("--python", default=sys.executable,
                            help="Python executable to create venv with")
        p_venv.add_argument(
            "-r",
            "--requirements",
            default=None,
            help="Requirements file to install (defaults to requirements.txt if present)",
        )
        p_venv.add_argument("--upgrade", action="store_true",
                            help="Upgrade pip/setuptools/wheel after creation")
        p_venv.add_argument(
            "--no-install",
            action="store_true",
            help="Do not install dependencies even if requirements file exists",
        )

        # build command
        p_build = subparsers.add_parser(
            "build", help="Build distribution artifacts")
        p_build.add_argument("--use-venv", action="store_true",
                             help="Use the project's .venv python if available")
        p_build.add_argument(
            "--sdist-only", action="store_true", help="Build sdist only")
        p_build.add_argument(
            "--wheel-only", action="store_true", help="Build wheel only")
        p_build.add_argument(
            "--extra-args",
            default="",
            help="Extra arguments passed to python -m build or setup.py",
        )

        # clean command
        p_clean = subparsers.add_parser("clean", help="Remove build artifacts")
        p_clean.add_argument("--all", action="store_true",
                             help="Also remove .venv")

        # default to build if no command
        parser.set_defaults(command="build")

        return parser

    def _run_command(self, cmd: str, method: Callable[[str], None] | None = None, **kwargs: Dict[str, Any]) -> int:
        env = kwargs.pop("env", None)
        cwd = kwargs.pop("cwd", None)
        shell = kwargs.pop("shell", True)

        proc = subprocess.Popen(
            cmd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            cwd=cwd,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            if method:
                method(line.rstrip("\n"))
            else:
                if not (self.args and self.args.quiet):
                    print(line, end="")
        proc.wait()
        return int(proc.returncode or 0)

    def _venv_python(self) -> Optional[str]:
        if not self.venv_dir.exists():
            return None
        if os.name == "nt":
            py = self.venv_dir / "Scripts" / "python.exe"
        else:
            py = self.venv_dir / "bin" / "python"
        return str(py) if py.exists() else None

    def _set_up_venv(self) -> int:
        assert self.args is not None
        py_exe = getattr(self.args, "python", sys.executable)

        if not self.venv_dir.exists():
            rc = self._run_command(f'"{py_exe}" -m venv "{self.venv_dir}"')
            if rc != 0:
                return rc

        vpy = self._venv_python()
        if not vpy:
            return 1

        if self.args.upgrade:
            rc = self._run_command(
                f'"{vpy}" -m pip install --upgrade pip setuptools wheel')
            if rc != 0:
                return rc

        if not getattr(self.args, "no_install", False):
            req = self.args.requirements
            if req is None:
                default_req = self.root_dir / "requirements.txt"
                req = str(default_req) if default_req.exists() else None
            if req:
                rc = self._run_command(f'"{vpy}" -m pip install -r "{req}"')
                if rc != 0:
                    return rc
        return 0

    def _build(self) -> int:
        assert self.args is not None

        python_exec = sys.executable
        if getattr(self.args, "use_venv", False):
            vpy = self._venv_python()
            if vpy:
                python_exec = vpy

        extra = getattr(self.args, "extra_args", "") or ""
        flags = []
        if getattr(self.args, "sdist_only", False):
            flags.append("--sdist")
        if getattr(self.args, "wheel_only", False):
            flags.append("--wheel")

        cmd_build = f'"{python_exec}" -m build {" ".join(flags)} {extra}'.strip(
        )
        rc = self._run_command(cmd_build)
        if rc == 0:
            return 0

        setup_py = self.root_dir / "setup.py"
        if setup_py.exists():
            targets = []
            if getattr(self.args, "sdist_only", False):
                targets.append("sdist")
            if getattr(self.args, "wheel_only", False):
                targets.append("bdist_wheel")
            if not targets:
                targets = ["sdist", "bdist_wheel"]
            cmd_setup = f'"{python_exec}" "{setup_py}" {" ".join(targets)} {extra}'.strip(
            )
            return self._run_command(cmd_setup)

        return rc

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        artifacts = [
            self.root_dir / "build",
            self.root_dir / "dist",
        ]
        # remove any *.egg-info directories
        for p in self.root_dir.iterdir():
            if p.name.endswith(".egg-info"):
                artifacts.append(p)

        rc = 0
        for path in artifacts:
            try:
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
                elif path.exists():
                    path.unlink(missing_ok=True)  # type: ignore[arg-type]
            except Exception:
                rc = 1

        if self.args and getattr(self.args, "all", False):
            try:
                if self.venv_dir.exists():
                    shutil.rmtree(self.venv_dir, ignore_errors=True)
            except Exception:
                rc = 1

        return rc

    def main(self) -> int:
        self.args = self.parser.parse_args()

        if self.args.command == "venv":
            return self._set_up_venv()
        if self.args.command == "clean":
            return self._clean()
        if self.args.command == "build":
            return self._build()
        return 1
