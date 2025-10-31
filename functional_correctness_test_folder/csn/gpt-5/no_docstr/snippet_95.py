from __future__ import annotations
import contextlib

import asyncio
import os
import shlex
import sys
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence, Union


@dataclass
class Command:
    args: Union[str, Sequence[str]]
    shell: bool = False
    cwd: Optional[str] = None
    env: Optional[Mapping[str, str]] = None
    timeout: Optional[float] = None
    stdin_data: Optional[bytes] = None
    capture_output: bool = True

    # Execution results
    returncode: Optional[int] = None
    stdout: Optional[bytes] = None
    stderr: Optional[bytes] = None

    async def execute(self) -> None:
        stdout_pipe = asyncio.subprocess.PIPE if self.capture_output else None
        stderr_pipe = asyncio.subprocess.PIPE if self.capture_output else None
        stdin_pipe = asyncio.subprocess.PIPE if self.stdin_data is not None else None

        # Build environment
        env = None
        if self.env is not None:
            env = os.environ.copy()
            env.update({str(k): str(v) for k, v in self.env.items()})

        if self.shell:
            if isinstance(self.args, (list, tuple)):
                cmd_str = " ".join(shlex.quote(str(x)) for x in self.args)
            else:
                cmd_str = str(self.args)
            proc = await asyncio.create_subprocess_shell(
                cmd_str,
                stdout=stdout_pipe,
                stderr=stderr_pipe,
                stdin=stdin_pipe,
                cwd=self.cwd,
                env=env,
            )
        else:
            if isinstance(self.args, str):
                # If a single string is given and shell=False, split safely
                argv = shlex.split(self.args)
            else:
                argv = [str(x) for x in self.args]
            proc = await asyncio.create_subprocess_exec(
                *argv,
                stdout=stdout_pipe,
                stderr=stderr_pipe,
                stdin=stdin_pipe,
                cwd=self.cwd,
                env=env,
            )

        try:
            if self.timeout is not None and self.timeout > 0:
                self.stdout, self.stderr = await asyncio.wait_for(
                    proc.communicate(input=self.stdin_data), timeout=self.timeout
                )
            else:
                self.stdout, self.stderr = await proc.communicate(input=self.stdin_data)
        except asyncio.TimeoutError:
            with contextlib.suppress(ProcessLookupError):
                proc.kill()
            await proc.wait()
            self.returncode = -1
            if self.capture_output:
                if self.stdout is None:
                    self.stdout = b""
                if self.stderr is None:
                    self.stderr = b""
                self.stderr += b"\nProcess timed out"
            return

        self.returncode = proc.returncode


# Optional import used in Command.execute


class AsyncCmdStep:
    def __init__(self, name: str, context: Any, is_shell: bool = False) -> None:
        self.name = name
        self.context = context
        self.is_shell = is_shell
        self._command: Optional[Command] = None

    def create_command(self, cmd_input: Mapping) -> Command:
        # Extract command/args
        cmd: Union[str, Sequence[str], None] = None
        if "cmd" in cmd_input:
            cmd = cmd_input["cmd"]  # could be str or list
        elif "args" in cmd_input:
            cmd = cmd_input["args"]

        if cmd is None:
            raise ValueError("cmd_input must include 'cmd' or 'args'")

        # Determine shell mode
        shell = bool(cmd_input.get("shell", self.is_shell))
        # Normalize args
        if shell:
            # shell accepts string; if list is given, join safely
            if isinstance(cmd, (list, tuple)):
                args: Union[str, Sequence[str]] = " ".join(
                    shlex.quote(str(x)) for x in cmd
                )
            else:
                args = str(cmd)
        else:
            # exec mode prefers a list of strings
            if isinstance(cmd, str):
                args = cmd  # will be split in Command if needed
            else:
                args = [str(x) for x in cmd]

        cwd = cmd_input.get("cwd")
        env = cmd_input.get("env")
        timeout_val = cmd_input.get("timeout")
        timeout: Optional[float] = None
        if timeout_val is not None:
            try:
                timeout = float(timeout_val)
            except (TypeError, ValueError):
                raise ValueError("timeout must be a number (seconds)")

        stdin_data = cmd_input.get("stdin")
        if isinstance(stdin_data, str):
            stdin_bytes = stdin_data.encode("utf-8")
        elif isinstance(stdin_data, (bytes, bytearray)):
            stdin_bytes = bytes(stdin_data)
        elif stdin_data is None:
            stdin_bytes = None
        else:
            raise ValueError("stdin must be str, bytes, or None")

        capture_output = bool(cmd_input.get("capture_output", True))

        command = Command(
            args=args,
            shell=shell,
            cwd=cwd,
            env=env,
            timeout=timeout,
            stdin_data=stdin_bytes,
            capture_output=capture_output,
        )
        self._command = command
        return command

    def run_step(self) -> None:
        if self._command is None:
            raise RuntimeError(
                "No command created. Call create_command() first.")

        def log_info(msg: str) -> None:
            logger = getattr(self.context, "logger", None)
            if logger and hasattr(logger, "info"):
                logger.info(msg)
                return
            log_func = getattr(self.context, "log", None)
            if callable(log_func):
                log_func(msg)
                return
            # Fallback to stdout
            print(msg, file=sys.stdout)

        def log_error(msg: str) -> None:
            logger = getattr(self.context, "logger", None)
            if logger and hasattr(logger, "error"):
                logger.error(msg)
                return
            log_func = getattr(self.context, "error", None)
            if callable(log_func):
                log_func(msg)
                return
            print(msg, file=sys.stderr)

        log_info(f"[{self.name}] Starting command")
        try:
            asyncio.run(self._command.execute())
        except RuntimeError as e:
            # In case we're already in an event loop (e.g., inside another async framework)
            if "asyncio.run() cannot be called from a running event loop" in str(e):
                async def _run():
                    await self._command.execute()
                # Use nested loop via asyncio.run in a thread-safe way
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Create a new task and wait for it
                    fut = asyncio.run_coroutine_threadsafe(_run(), loop)
                    fut.result()
                else:
                    loop.run_until_complete(_run())
            else:
                raise

        rc = self._command.returncode
        stdout = (self._command.stdout or b"").decode(
            "utf-8", errors="replace")
        stderr = (self._command.stderr or b"").decode(
            "utf-8", errors="replace")

        if stdout:
            log_info(f"[{self.name}] stdout:\n{stdout.rstrip()}")
        if stderr:
            log_error(f"[{self.name}] stderr:\n{stderr.rstrip()}")

        if rc != 0:
            raise RuntimeError(
                f"[{self.name}] Command failed with exit code {rc}")
