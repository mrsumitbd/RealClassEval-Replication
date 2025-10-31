from typing import Any, Callable, Dict, Optional
from argparse import ArgumentParser
import argparse
import subprocess
import sys
import os
import shutil
import logging
import glob
from pathlib import Path


class Build:
    '''
    Build class
    '''

    def __init__(self) -> None:
        '''
        Constructor
        '''
        self.logger = logging.getLogger(self.__class__.__name__)
        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        self.parser = self._set_up_parser()
        self.args: Optional[argparse.Namespace] = None

    def _set_up_parser(self) -> ArgumentParser:
        '''
        Set up argument parser
        :return: Argument parser
        :rtype: argparse.ArgumentParser
        '''
        parser = ArgumentParser(prog="build", description="Build utilities")
        parser.add_argument("-v", "--verbose",
                            action="store_true", help="Enable verbose logging")
        parser.add_argument("-q", "--quiet", action="store_true",
                            help="Suppress non-error logs")

        subparsers = parser.add_subparsers(dest="command", required=False)

        # venv subcommand
        p_venv = subparsers.add_parser(
            "venv", help="Set up a Python virtual environment")
        p_venv.add_argument("--venv", default=".venv",
                            help="Virtual environment directory (default: .venv)")
        p_venv.add_argument("--python", default=sys.executable,
                            help="Python executable to create venv (default: current interpreter)")
        p_venv.add_argument("--requirements", default=None,
                            help="Requirements file path (default: requirements.txt if exists)")

        # build subcommand
        p_build = subparsers.add_parser(
            "build", help="Build from a spec file using PyInstaller")
        p_build.add_argument(
            "--spec", default=None, help="Path to .spec file (default: first *.spec in CWD)")
        p_build.add_argument("--venv", default=".venv",
                             help="Virtual environment directory (default: .venv)")
        p_build.add_argument("--pyinstaller", default=None,
                             help="PyInstaller executable or module (default: use venv if available, else system)")
        p_build.add_argument("pyinstaller_args", nargs=argparse.REMAINDER,
                             help="Additional arguments passed to PyInstaller")

        # clean subcommand
        subparsers.add_parser(
            "clean", help="Delete build directories (build/, dist/)")

        # all subcommand: venv then build
        p_all = subparsers.add_parser(
            "all", help="Create venv (if needed) and build")
        p_all.add_argument("--venv", default=".venv",
                           help="Virtual environment directory (default: .venv)")
        p_all.add_argument("--python", default=sys.executable,
                           help="Python executable to create venv (default: current interpreter)")
        p_all.add_argument("--requirements", default=None,
                           help="Requirements file path (default: requirements.txt if exists)")
        p_all.add_argument(
            "--spec", default=None, help="Path to .spec file (default: first *.spec in CWD)")
        p_all.add_argument("--pyinstaller", default=None,
                           help="PyInstaller executable or module (default: use venv if available, else system)")
        p_all.add_argument("pyinstaller_args", nargs=argparse.REMAINDER,
                           help="Additional arguments passed to PyInstaller")

        return parser

    def _run_command(self, cmd: str, method: Callable[[str], None] = None, **kwargs: Dict[str, Any]) -> int:
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
        log = method if method is not None else self.logger.info
        try:
            with subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                **kwargs
            ) as proc:
                if proc.stdout is not None:
                    for line in proc.stdout:
                        if line:
                            log(line.rstrip())
                proc.wait()
                return proc.returncode if proc.returncode is not None else 1
        except FileNotFoundError as e:
            self.logger.error(f"Command not found: {cmd} ({e})")
            return 127
        except Exception as e:
            self.logger.error(f"Error running command: {cmd} ({e})")
            return 1

    def _set_up_venv(self) -> int:
        '''
        Set up a Python virtual environment
        :return: Return code
        :rtype: int
        '''
        assert self.args is not None
        venv_dir = Path(getattr(self.args, "venv", ".venv"))
        python_exec = getattr(self.args, "python", sys.executable)
        requirements_arg = getattr(self.args, "requirements", None)

        # Create venv if missing
        if not venv_dir.exists():
            self.logger.info(
                f"Creating virtual environment at {venv_dir} using {python_exec}")
            rc = self._run_command(f'"{python_exec}" -m venv "{venv_dir}"')
            if rc != 0:
                return rc
        else:
            self.logger.info(
                f"Virtual environment already exists at {venv_dir}")

        # Determine venv python
        venv_python = venv_dir / ("Scripts" if os.name == "nt" else "bin") / \
            ("python.exe" if os.name == "nt" else "python")
        if not venv_python.exists():
            self.logger.error(
                f"Virtual environment seems broken: {venv_python} not found")
            return 1

        # Upgrade pip
        self.logger.info("Upgrading pip in virtual environment")
        rc = self._run_command(f'"{venv_python}" -m pip install --upgrade pip')
        if rc != 0:
            return rc

        # Install requirements if provided or default file exists
        requirements_file: Optional[Path] = None
        if requirements_arg:
            requirements_file = Path(requirements_arg)
        else:
            default_req = Path("requirements.txt")
            if default_req.exists():
                requirements_file = default_req

        if requirements_file and requirements_file.exists():
            self.logger.info(
                f"Installing requirements from {requirements_file}")
            rc = self._run_command(
                f'"{venv_python}" -m pip install -r "{requirements_file}"')
            if rc != 0:
                return rc
        elif requirements_arg:
            self.logger.error(
                f"Requirements file not found: {requirements_arg}")
            return 1

        return 0

    def _build(self) -> int:
        '''
        Build from a spec file
        :return: Return code
        :rtype: int
        '''
        assert self.args is not None

        spec_path = getattr(self.args, "spec", None)
        if not spec_path:
            specs = sorted(glob.glob("*.spec"))
            if not specs:
                self.logger.error(
                    "No .spec file provided and none found in current directory")
                return 1
            spec_path = specs[0]
        spec = Path(spec_path)
        if not spec.exists():
            self.logger.error(f"Spec file not found: {spec}")
            return 1

        # Determine pyinstaller executable
        venv_dir = Path(getattr(self.args, "venv", ".venv"))
        pyinstaller_arg = getattr(self.args, "pyinstaller", None)
        if pyinstaller_arg:
            pyinstaller_cmd = pyinstaller_arg
        else:
            venv_pyinstaller = venv_dir / ("Scripts" if os.name == "nt" else "bin") / (
                "pyinstaller.exe" if os.name == "nt" else "pyinstaller")
            if venv_pyinstaller.exists():
                pyinstaller_cmd = f'"{venv_pyinstaller}"'
            else:
                # Try using module via current interpreter or system pyinstaller
                pyinstaller_cmd = f'"{sys.executable}" -m PyInstaller'

        extra_args = getattr(self.args, "pyinstaller_args", []) or []
        extra = ""
        if extra_args:
            # Drop leading '--' if present (from REMAINDER usage)
            if len(extra_args) > 0 and extra_args[0] == "--":
                extra_args = extra_args[1:]
            extra = " " + " ".join(extra_args)

        cmd = f'{pyinstaller_cmd} "{spec}"{extra}'
        self.logger.info(f"Running: {cmd}")
        rc = self._run_command(cmd)
        return rc

    def _clean(self) -> int:
        '''
        Delete build directories
        :return: Return code
        :rtype: int
        '''
        dirs = [Path("build"), Path("dist")]
        ret = 0
        for d in dirs:
            if d.exists():
                try:
                    shutil.rmtree(d)
                    self.logger.info(f"Removed {d}")
                except Exception as e:
                    self.logger.error(f"Failed to remove {d}: {e}")
                    ret = 1
            else:
                self.logger.info(f"Directory not found, skipping: {d}")
        return ret

    def main(self) -> int:
        '''
        Build
        :return: Return code
        :rtype: int
        '''
        self.args = self.parser.parse_args()

        # Configure logging level
        if getattr(self.args, "quiet", False):
            self.logger.setLevel(logging.ERROR)
        elif getattr(self.args, "verbose", False):
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        cmd = getattr(self.args, "command", None)

        if cmd == "venv":
            return self._set_up_venv()
        elif cmd == "clean":
            return self._clean()
        elif cmd == "build":
            return self._build()
        elif cmd == "all":
            rc = self._set_up_venv()
            if rc != 0:
                return rc
            return self._build()
        else:
            # Default action: build
            return self._build()
