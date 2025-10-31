import argparse
import shlex
from typing import Any


class DependenciesConfiguration:
    '''Dependency configuration class, for RuntimeContext.job_script_provider.'''

    def __init__(self, args: argparse.Namespace) -> None:
        '''Initialize.'''
        self.python: str = getattr(args, "python", "python3")
        self.venv: str | None = getattr(args, "venv", None)
        self.requirements: str | None = getattr(args, "requirements", None)
        self.packages: list[str] = list(getattr(args, "packages", []) or [])
        self.pre_commands: list[str] = list(
            getattr(args, "pre_commands", []) or [])
        self.post_commands: list[str] = list(
            getattr(args, "post_commands", []) or [])
        self.upgrade_pip: bool = bool(getattr(args, "upgrade_pip", True))
        self.install_command: str = getattr(
            args, "install_command", "pip install")

    def build_job_script(self, builder: 'Builder', command: list[str]) -> str:
        lines: list[str] = []
        lines.append("set -euo pipefail")

        # Pre-commands
        for cmd in self.pre_commands:
            if cmd.strip():
                lines.append(cmd)

        # Virtual environment setup
        if self.venv:
            venv_bin = f"{self.venv}/bin"
            lines.append(
                f'{shlex.quote(self.python)} -m venv {shlex.quote(self.venv)} || true')
            lines.append(f'. {shlex.quote(venv_bin)}/activate')
            if self.upgrade_pip:
                lines.append(
                    "python -m pip install --upgrade pip setuptools wheel")
            pip_prefix = ""
        else:
            # No venv; still optionally upgrade pip
            if self.upgrade_pip:
                lines.append(
                    f'{shlex.quote(self.python)} -m pip install --upgrade pip setuptools wheel')
            pip_prefix = f'{shlex.quote(self.python)} -m '

        # Dependency installation
        if self.requirements:
            lines.append(
                f'{pip_prefix}{self.install_command} -r {shlex.quote(self.requirements)}')

        if self.packages:
            pkg_args = " ".join(shlex.quote(p) for p in self.packages)
            lines.append(f'{pip_prefix}{self.install_command} {pkg_args}')

        # Main command
        if command:
            lines.append(shlex.join(command))

        # Post-commands
        for cmd in self.post_commands:
            if cmd.strip():
                lines.append(cmd)

        return "\n".join(lines) + "\n"
