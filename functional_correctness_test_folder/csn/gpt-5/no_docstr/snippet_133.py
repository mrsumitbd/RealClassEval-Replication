import argparse
import shlex
import sys
from typing import Any, Dict, Iterable, List, Optional


class DependenciesConfiguration:
    def __init__(self, args: argparse.Namespace) -> None:
        # Resolve python executable
        self.python_executable: str = getattr(args, "python", sys.executable)

        # Dependencies handling
        pkgs = getattr(args, "packages", None)
        if pkgs is None:
            pkgs = getattr(args, "deps", None)
        self.packages: List[str] = list(pkgs) if pkgs else []

        self.requirements_file: Optional[str] = getattr(
            args, "requirements", None)
        self.enable_pip_install: bool = bool(
            getattr(args, "pip_install", True))

        # Environment variables
        env = getattr(args, "env", None)
        self.env: Dict[str, str] = dict(env) if isinstance(env, dict) else {}

        # Optional module system (e.g., LMOD)
        modules = getattr(args, "modules", None)
        self.modules: List[str] = list(modules) if modules else []

        # Extra setup commands (optional hook)
        setup_cmds = getattr(args, "setup", None)
        self.setup_commands: List[str] = list(setup_cmds) if setup_cmds else []

    def build_job_script(self, builder: "Builder", command: List[str]) -> str:
        lines: List[str] = ["#!/usr/bin/env bash", "set -euo pipefail"]

        # Load modules if requested (only if `module` command is available)
        if self.modules:
            lines.append('if command -v module >/dev/null 2>&1; then')
            for mod in self.modules:
                lines.append(f"  module load {shlex.quote(mod)}")
            lines.append("fi")

        # Export environment variables
        for k, v in self.env.items():
            key = str(k)
            val = "" if v is None else str(v)
            lines.append(f"export {key}={shlex.quote(val)}")

        # Additional setup commands, if any
        for cmd in self.setup_commands:
            lines.append(cmd)

        # Pip install dependencies if enabled
        if self.enable_pip_install and (self.requirements_file or self.packages):
            pip_cmd = f"{shlex.quote(self.python_executable)} -m pip"
            lines.append(f"{pip_cmd} install --upgrade pip")
            if self.requirements_file:
                lines.append(
                    f"{pip_cmd} install -r {shlex.quote(self.requirements_file)}")
            if self.packages:
                pkg_str = " ".join(shlex.quote(p) for p in self.packages)
                lines.append(f"{pip_cmd} install {pkg_str}")

        # Final command
        if not command:
            raise ValueError("command must be a non-empty list of strings")
        quoted_cmd = " ".join(shlex.quote(part) for part in command)
        lines.append(f"exec {quoted_cmd}")

        return "\n".join(lines) + "\n"
