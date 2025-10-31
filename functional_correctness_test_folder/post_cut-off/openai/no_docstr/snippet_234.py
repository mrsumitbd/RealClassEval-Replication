
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Callable, Dict, Any

from argparse import ArgumentParser, Namespace


class Build:
    def __init__(self) -> None:
        self.parser = self._set_up_parser()
        self.args: Namespace = self.parser.parse_args()

    def _set_up_parser(self) -> ArgumentParser:
        parser = ArgumentParser(
            prog="build",
            description="Utility to set up virtual environment, build package, and clean artifacts.",
        )
        subparsers = parser.add_subparsers(dest="command", required=True)

        # Setup virtual environment
        venv_parser = subparsers.add_parser(
            "setup-venv",
            help="Create a virtual environment and install dependencies.",
        )
        venv_parser.add_argument(
            "--venv-dir",
            default="venv",
            help="Directory for the virtual environment (default: venv).",
        )
        venv_parser.add_argument(
            "--requirements",
            default="requirements.txt",
            help="Requirements file to install (default: requirements.txt).",
        )

        # Build package
        build_parser = subparsers.add_parser(
            "build",
            help="Build the package using the standard build module.",
        )
        build_parser.add_argument(
            "--build-dir",
            default="build",
            help="Build directory (default: build).",
        )
        build_parser.add_argument(
            "--dist-dir",
            default="dist",
            help="Distribution directory (default: dist).",
        )

        # Clean artifacts
        clean_parser = subparsers.add_parser(
            "clean",
            help="Remove build artifacts and optionally the virtual environment.",
        )
        clean_parser.add_argument(
            "--venv-dir",
            default="venv",
            help="Virtual environment directory to remove (default: venv).",
        )
        clean_parser.add_argument(
            "--all",
            action="store_true",
            help="Remove all build artifacts including venv.",
        )

        return parser

    def _run_command(
        self,
        cmd: str,
        method: Callable[[str], None] = None,
        **kwargs: Dict[str, Any],
    ) -> int:
        """Run a shell command and optionally process its output."""
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
        venv_dir = Path(self.args.venv_dir).resolve()
        req_file = Path(self.args.requirements).resolve()

        # Create virtual environment
        if not venv_dir.exists():
            print(f"Creating virtual environment at {venv_dir}")
            ret = self._run_command(f"{sys.executable} -m venv {venv_dir}")
            if ret != 0:
                return ret

        # Install dependencies
        if req_file.exists():
            pip_exe = venv_dir / ("Scripts" if os.name ==
                                  "nt" else "bin") / "pip"
            print(f"Installing dependencies from {req_file}")
            ret = self._run_command(f"{pip_exe} install -r {req_file}")
            if ret != 0:
                return ret
        else:
            print(
                f"No requirements file found at {req_file}, skipping install.")
        return 0

    def _build(self) -> int:
        build_dir = Path(self.args.build_dir).resolve()
        dist_dir = Path(self.args.dist_dir).resolve()

        # Ensure build and dist directories exist
        build_dir.mkdir(parents=True, exist_ok=True)
        dist_dir.mkdir(parents=True, exist_ok=True)

        # Run the build
        print(f"Building package into {dist_dir}")
        ret = self._run_command(
            f"{sys.executable} -m build --sdist --wheel --outdir {dist_dir}")
        return ret

    def _clean(self) -> int:
        dirs_to_remove = ["build", "dist"]
        patterns = ["*.egg-info", "*.egg", "*.dist-info"]

        # Remove build and dist directories
        for d in dirs_to_remove:
            path = Path(d)
            if path.exists() and path.is_dir():
                print(f"Removing directory {path}")
                shutil.rmtree(path, ignore_errors=True)

        # Remove egg-info directories
        for pattern in patterns:
            for p in Path(".").glob(pattern):
                if p.is_dir():
                    print(f"Removing directory {p}")
                    shutil.rmtree(p, ignore_errors=True)

        # Optionally remove virtual environment
        if self.args.all:
            venv_dir = Path(self.args.venv_dir).resolve()
            if venv_dir.exists() and venv_dir.is_dir():
                print(f"Removing virtual environment {venv_dir}")
                shutil.rmtree(venv_dir, ignore_errors=True)

        return 0

    def main(self) -> int:
        cmd = self.args.command
        if cmd == "setup-venv":
            return self._set_up_venv()
        elif cmd == "build":
            return self._build()
        elif cmd == "clean":
            return self._clean()
        else:
            self.parser.print_help()
            return 1


if __name__ == "__main__":
    build_tool = Build()
    sys.exit(build_tool.main())
