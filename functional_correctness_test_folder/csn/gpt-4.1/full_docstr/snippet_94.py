
import subprocess
import sys
import logging
import os
from pathlib import Path
from typing import Any, Mapping, List, Union

# Dummy stubs for pypyr classes for this implementation.
# In real usage, these would be imported from pypyr packages.


class Context(dict):
    pass


class Command:
    def __init__(
        self,
        run: Union[str, List[str]],
        save: bool = False,
        cwd: Union[str, Path, None] = None,
        bytes_: bool = False,
        encoding: Union[str, None] = None,
        stdout: Union[str, Path, None] = None,
        stderr: Union[str, Path, None] = None,
        append: bool = False,
    ):
        self.run = run
        self.save = save
        self.cwd = cwd
        self.bytes = bytes_
        self.encoding = encoding
        self.stdout = stdout
        self.stderr = stderr
        self.append = append

    def __repr__(self):
        return (
            f"Command(run={self.run!r}, save={self.save!r}, cwd={self.cwd!r}, "
            f"bytes={self.bytes!r}, encoding={self.encoding!r}, "
            f"stdout={self.stdout!r}, stderr={self.stderr!r}, append={self.append!r})"
        )


class CmdStep:
    '''A pypyr step to run an executable or command as a subprocess.'''

    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
        self.name = name
        self.context = context
        self.is_shell = is_shell
        self.logger = logging.getLogger(name)
        self.commands: List[Command] = []

        cmd_input = context.get('cmd')
        if cmd_input is None:
            raise ValueError("No 'cmd' found in context for CmdStep.")

        self.commands = self._parse_cmd_input(cmd_input)

    def _parse_cmd_input(self, cmd_input: Any) -> List[Command]:
        # Helper to parse the cmd input into a list of Command objects.
        commands = []
        if isinstance(cmd_input, str):
            # Simplified syntax: single string
            commands.append(Command(run=cmd_input))
        elif isinstance(cmd_input, list):
            # List of commands, each can be string or dict
            for item in cmd_input:
                if isinstance(item, str):
                    commands.append(Command(run=item))
                elif isinstance(item, dict):
                    commands.extend(self._parse_expanded(item))
                else:
                    raise ValueError(f"Invalid cmd list item: {item!r}")
        elif isinstance(cmd_input, dict):
            # Expanded syntax
            commands.extend(self._parse_expanded(cmd_input))
        else:
            raise ValueError(f"Invalid cmd input: {cmd_input!r}")
        return commands

    def _parse_expanded(self, cmd_dict: Mapping) -> List[Command]:
        # Parse expanded syntax dict, which may have 'run' as str or list
        run = cmd_dict.get('run')
        if run is None:
            raise ValueError("Expanded cmd dict must have 'run' key.")

        save = bool(cmd_dict.get('save', False))
        cwd = cmd_dict.get('cwd')
        bytes_ = bool(cmd_dict.get('bytes', False))
        encoding = cmd_dict.get('encoding')
        stdout = cmd_dict.get('stdout')
        stderr = cmd_dict.get('stderr')
        append = bool(cmd_dict.get('append', False))

        if isinstance(run, str):
            return [Command(run=run, save=save, cwd=cwd, bytes_=bytes_, encoding=encoding,
                            stdout=stdout, stderr=stderr, append=append)]
        elif isinstance(run, list):
            return [
                Command(run=cmd, save=save, cwd=cwd, bytes_=bytes_, encoding=encoding,
                        stdout=stdout, stderr=stderr, append=append)
                for cmd in run
            ]
        else:
            raise ValueError(f"Invalid 'run' value in expanded cmd: {run!r}")

    def create_command(self, cmd_input: Mapping) -> Command:
        # Only for expanded syntax
        return self._parse_expanded(cmd_input)[0]

    def run_step(self) -> None:
        cmd_outs = []
        for cmd in self.commands:
            self.logger.info(f"Running command: {cmd.run!r}")
            result = self._run_command(cmd)
            if cmd.save:
                cmd_outs.append(result)
        if any(cmd.save for cmd in self.commands):
            # If only one, save as dict, else as list
            if len(cmd_outs) == 1:
                self.context['cmdOut'] = cmd_outs[0]
            else:
                self.context['cmdOut'] = cmd_outs

    def _run_command(self, cmd: Command) -> dict:
        # Prepare stdout/stderr redirection
        stdout_file = None
        stderr_file = None
        stdout_target = None
        stderr_target = None

        def open_file(path, append):
            mode = 'ab' if append else 'wb'
            return open(path, mode)

        # Handle special values for stdout/stderr
        if cmd.stdout:
            if cmd.stdout == '/dev/null':
                stdout_target = open(os.devnull, 'wb')
            else:
                stdout_target = open_file(cmd.stdout, cmd.append)
        if cmd.stderr:
            if cmd.stderr == '/dev/null':
                stderr_target = open(os.devnull, 'wb')
            elif cmd.stderr == '/dev/stdout':
                stderr_target = subprocess.STDOUT
            else:
                stderr_target = open_file(cmd.stderr, cmd.append)

        # Prepare the command
        if isinstance(cmd.run, str):
            run_cmd = cmd.run
        else:
            run_cmd = cmd.run

        # Run the subprocess
        try:
            completed = subprocess.run(
                run_cmd,
                shell=self.is_shell,
                cwd=cmd.cwd,
                stdout=stdout_target if stdout_target is not None else subprocess.PIPE if cmd.save else None,
                stderr=stderr_target if (stderr_target is not None and stderr_target !=
                                         subprocess.STDOUT) else subprocess.PIPE if cmd.save else None,
                check=False,
                encoding=None if cmd.bytes else (
                    cmd.encoding if cmd.encoding else None),
            )
        finally:
            if stdout_target and hasattr(stdout_target, 'close'):
                stdout_target.close()
            if stderr_target and hasattr(stderr_target, 'close') and stderr_target != subprocess.STDOUT:
                stderr_target.close()

        # Save output if needed
        if cmd.save:
            # stdout
            if cmd.bytes:
                stdout_val = completed.stdout if completed.stdout is not None else None
                stderr_val = completed.stderr if completed.stderr is not None else None
            else:
                stdout_val = completed.stdout if completed.stdout is not None else None
                stderr_val = completed.stderr if completed.stderr is not None else None
                # Remove trailing newlines
                if stdout_val is not None:
                    stdout_val = stdout_val.rstrip('\r\n')
                if stderr_val is not None:
                    stderr_val = stderr_val.rstrip('\r\n')
            return {
                'returncode': completed.returncode,
                'stdout': stdout_val if stdout_val != '' else None,
                'stderr': stderr_val if stderr_val != '' else None,
            }
        return {}
