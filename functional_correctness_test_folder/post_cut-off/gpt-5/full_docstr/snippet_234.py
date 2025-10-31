import argparse
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Dict, Optional


class Build:
    '''
    Build class
    '''

    def __init__(self) -> None:
        '''
        Constructor
        '''
        self.root: Path = Path.cwd()
        self.venv_dir: Path = self.root / ".venv"
        self.logger = logging.getLogger("build")
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter("[%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        self.parser = self._set_up_parser()

    def _set_up_parser(self) -> argparse.ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = argparse.ArgumentParser(
            prog="build", description="Build helper")
        mx = parser.add_mutually_exclusive_group()
        mx.add_argument("--venv", action="store_true",
                        help="Set up a Python virtual environment")
        mx.add_argument("--build", action="store_true",
                        help="Build project (default action)")
        mx.add_argument("--clean", action="store_true",
                        help="Clean build artifacts")
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose logging",
        )
        return parser

    def _run_command(self, cmd: str, method: Optional[Callable[[str], None]] = None, **kwargs: Dict[str, Any]) -> int:
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
        logger_method = method if method is not None else self.logger.info
        try:
            with subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                **kwargs,
            ) as proc:
                if proc.stdout:
                    for line in proc.stdout:
                        logger_method(line.rstrip())
                proc.wait()
                return proc.returncode if proc.returncode is not None else 1
        except FileNotFoundError as e:
            self.logger.error(f"Command not found: {e}")
            return 127
        except Exception as e:
            self.logger.error(f"Error running command '{cmd}': {e}")
            return 1

    def _python_executable(self) -> str:
        if self.venv_dir.exists():
            if os.name == "nt":
                candidate = self.venv_dir / "Scripts" / "python.exe"
            else:
                candidate = self.venv_dir / "bin" / "python"
            if candidate.exists():
                return str(candidate)
        return sys.executable

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        try:
            import venv  # noqa: F401
        except Exception as e:
            self.logger.error(f"Cannot import venv module: {e}")
            return 1

        if self.venv_dir.exists():
            self.logger.info(
                f"Virtual environment already exists at {self.venv_dir}")
        else:
            self.logger.info(
                f"Creating virtual environment at {self.venv_dir}...")
            try:
                import venv
                builder = venv.EnvBuilder(
                    with_pip=True, clear=False, upgrade=False, symlinks=True)
                builder.create(str(self.venv_dir))
            except Exception as e:
                self.logger.error(f"Failed to create virtual environment: {e}")
                return 1

        py = self._python_executable()
        self.logger.info("Upgrading pip...")
        rc = self._run_command(f'"{py}" -m pip install --upgrade pip')
        if rc != 0:
            return rc

        self.logger.info("Installing build tooling (build, wheel)...")
        rc = self._run_command(f'"{py}" -m pip install --upgrade build wheel')
        return rc

    def _build(self) -> int:
        '''
        Build from a spec file
        :return: Return code
        :rtype: int
        '''
        pyproject = self.root / "pyproject.toml"
        setup_py = self.root / "setup.py"

        if not pyproject.exists() and not setup_py.exists():
            self.logger.error(
                "No build specification found (pyproject.toml or setup.py).")
            return 2

        py = self._python_executable()

        self.logger.info("Building project...")
        rc = self._run_command(f'"{py}" -m build')
        if rc == 0:
            self.logger.info("Build completed successfully.")
        return rc

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        targets = [
            self.root / "build",
            self.root / "dist",
        ]
        # Remove *.egg-info directories
        targets.extend(self.root.glob("*.egg-info"))

        rc = 0
        for t in targets:
            if t.exists():
                try:
                    if t.is_dir():
                        shutil.rmtree(t)
                    else:
                        t.unlink()
                    self.logger.info(f"Removed {t}")
                except Exception as e:
                    self.logger.error(f"Failed to remove {t}: {e}")
                    rc = 1
        return rc

    def main(self) -> int:
        '''
        Build
        :return: Return code
        :rtype: int
        '''
        args = self.parser.parse_args()
        if getattr(args, "verbose", False):
            self.logger.setLevel(logging.DEBUG)

        if getattr(args, "venv", False):
            return self._set_up_venv()
        if getattr(args, "clean", False):
            return self._clean()

        # default action is build
        # ensure venv exists but do not create silently; use system python if not
        return self._build()
