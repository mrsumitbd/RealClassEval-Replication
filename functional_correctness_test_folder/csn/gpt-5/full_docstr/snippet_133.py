import argparse
import shlex
from typing import Any, Callable, Iterable, Mapping, Optional


class DependenciesConfiguration:
    '''Dependency configuration class, for RuntimeContext.job_script_provider.'''

    def __init__(self, args: argparse.Namespace) -> None:
        '''Initialize.'''
        self.shell: str = getattr(args, "job_shell", "/usr/bin/env bash")
        self.strict_bash: bool = bool(getattr(args, "strict_bash", True))
        self.working_directory: Optional[str] = getattr(
            args, "working_directory", None)

        self.prologue: list[str] = []
        prologue = getattr(args, "prologue", None)
        if isinstance(prologue, str):
            self.prologue = [prologue]
        elif isinstance(prologue, Iterable):
            self.prologue = [str(x) for x in prologue if x is not None]

        self.epilogue: list[str] = []
        epilogue = getattr(args, "epilogue", None)
        if isinstance(epilogue, str):
            self.epilogue = [epilogue]
        elif isinstance(epilogue, Iterable):
            self.epilogue = [str(x) for x in epilogue if x is not None]

        self.env: dict[str, str] = {}
        env = getattr(args, "env", None)
        if isinstance(env, Mapping):
            self.env = {str(k): str(v) for k, v in env.items()}
        elif isinstance(env, Iterable) and not isinstance(env, (str, bytes)):
            for item in env:
                if item is None:
                    continue
                if isinstance(item, str) and "=" in item:
                    k, v = item.split("=", 1)
                    self.env[k] = v
                elif isinstance(item, Mapping):
                    for k, v in item.items():
                        self.env[str(k)] = str(v)

    def _try_builder_interfaces(self, builder: Any, command: list[str]) -> Optional[str]:
        # Try common interfaces without enforcing galaxy-tool-util at import time
        # 1) builder.build(...)
        build_attr = getattr(builder, "build", None)
        if callable(build_attr):
            try:
                result = build_attr(command)
                if isinstance(result, str):
                    return result
            except TypeError:
                # Try with keyword names commonly used
                for kw in (
                    {"command": command},
                    {"cmd": command},
                    {"args": command},
                ):
                    try:
                        result = build_attr(**kw)
                        if isinstance(result, str):
                            return result
                    except Exception:
                        pass
            except Exception:
                pass

        # 2) Callable builder
        if callable(builder):
            try:
                result = builder(command)
                if isinstance(result, str):
                    return result
            except Exception:
                pass

        # 3) builder has method add_command + to_string
        add_cmd = getattr(builder, "add_command", None)
        to_string = getattr(builder, "to_string", None)
        if callable(add_cmd) and callable(to_string):
            try:
                add_cmd(command)
                result = to_string()
                if isinstance(result, str):
                    return result
            except Exception:
                pass

        return None

    def _compose_script(self, command: list[str]) -> str:
        if not command:
            raise ValueError("Command must be a non-empty list of strings.")
        lines: list[str] = []

        # Shebang
        # If shell is like "/usr/bin/env bash", use it directly; else default to env bash
        shebang = self.shell.strip() if self.shell else "/usr/bin/env bash"
        if not shebang.startswith("#!"):
            lines.append(f"#!{shebang}")
        else:
            lines.append(shebang)

        # Strict mode
        if self.strict_bash:
            lines.append("set -euo pipefail")

        # Export env vars
        for k, v in self.env.items():
            # Use printf-like safe export
            kv = f"{k}={v}"
            lines.append(f"export {shlex.quote(k)}={shlex.quote(v)}")

        # Change working directory
        if self.working_directory:
            lines.append(f"cd {shlex.quote(self.working_directory)}")

        # Prologue
        for line in self.prologue:
            if line is None:
                continue
            lines.append(str(line))

        # Main command
        lines.append(shlex.join(command))

        # Epilogue
        for line in self.epilogue:
            if line is None:
                continue
            lines.append(str(line))

        # Final newline
        return "\n".join(lines) + "\n"

    def build_job_script(self, builder: 'Builder', command: list[str]) -> str:
        '''Use the galaxy-tool-util library to construct a build script.'''
        # First, try to use the provided builder if it exposes familiar interfaces.
        script = self._try_builder_interfaces(builder, command)
        if isinstance(script, str) and script.strip():
            return script

        # Fallback to a simple shell script composition.
        return self._compose_script(command)
