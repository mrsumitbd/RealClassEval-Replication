
import asyncio
import subprocess
import sys
from typing import Mapping


class AsyncCmdStep:
    def __init__(self, name: str, context: "Context", is_shell: bool = False) -> None:
        self.name = name
        self.context = context
        self.is_shell = is_shell

    def create_command(self, cmd_input: Mapping) -> "Command":
        # Extract command components from the mapping
        cmd = cmd_input.get("cmd") or cmd_input.get("command")
        args = cmd_input.get("args", [])
        env = cmd_input.get("env", {})
        cwd = cmd_input.get("cwd")

        # Merge environment and cwd from context if available
        if hasattr(self.context, "env"):
            env = {**self.context.env, **env}
        if hasattr(self.context, "cwd") and cwd is None:
            cwd = self.context.cwd

        # Construct and return a Command instance
        return Command(cmd=cmd, args=args, env=env, cwd=cwd)

    async def _run_async(self, command: "Command") -> None:
        # Choose the appropriate subprocess creation method
        if self.is_shell:
            proc = await asyncio.create_subprocess_shell(
                command.cmd,
                env=command.env,
                cwd=command.cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        else:
            proc = await asyncio.create_subprocess_exec(
                command.cmd,
                *command.args,
                env=command.env,
                cwd=command.cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

        # Wait for the process to finish and capture output
        stdout, stderr = await proc.communicate()

        # Print stdout and stderr if present
        if stdout:
            print(stdout.decode(), end="")
        if stderr:
            print(stderr.decode(), file=sys.stderr, end="")

        # Raise an error if the command failed
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, command.cmd)

    def run_step(self) -> None:
        # Retrieve command input from the context
        cmd_input = getattr(self.context, "cmd_input", {})
        command = self.create_command(cmd_input)

        # Execute the command asynchronously
        asyncio.run(self._run_async(command))
