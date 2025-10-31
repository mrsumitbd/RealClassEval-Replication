
import logging
import os
from pathlib import Path
from typing import Any, Mapping, List, Union

# Dummy stubs for pypyr dependencies for this implementation.
# In real usage, these would be imported from pypyr.


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
        is_shell: bool = False,
    ):
        self.run = run
        self.save = save
        self.cwd = cwd
        self.bytes = bytes_
        self.encoding = encoding
        self.stdout = stdout
        self.stderr = stderr
        self.append = append
        self.is_shell = is_shell

    def run_command(self):
        import subprocess

        # Prepare command
        cmd = self.run
        if isinstance(cmd, str):
            cmd = cmd if self.is_shell else cmd.split()
        elif isinstance(cmd, list):
            if self.is_shell:
                cmd = " && ".join(cmd)
            else:
                # If not shell, flatten list of strings to list of args
                # Each item is a command string, so split each
                cmd = [item for sub in [c.split() for c in cmd]
                       for item in sub]

        # Prepare stdout/stderr
        def get_file_handle(path, mode):
            if path == "/dev/null":
                return open(os.devnull, mode)
            elif path is not None:
                return open(path, mode)
            else:
                return None

        stdout_handle = None
        stderr_handle = None
        stdout_mode = "ab" if self.append else "wb"
        stderr_mode = "ab" if self.append else "wb"
        try:
            if self.stdout:
                stdout_handle = get_file_handle(self.stdout, stdout_mode)
            if self.stderr:
                if self.stderr == "/dev/stdout":
                    stderr_handle = subprocess.STDOUT
                else:
                    stderr_handle = get_file_handle(self.stderr, stderr_mode)

            # Run the command
            completed = subprocess.run(
                cmd,
                shell=self.is_shell,
                cwd=str(self.cwd) if self.cwd else None,
                stdout=stdout_handle if stdout_handle else subprocess.PIPE,
                stderr=stderr_handle if (stderr_handle not in (
                    None, subprocess.STDOUT)) else subprocess.PIPE,
            )

            # Save output if required
            if self.save:
                if self.bytes:
                    stdout_val = completed.stdout if completed.stdout else None
                    stderr_val = completed.stderr if completed.stderr else None
                else:
                    encoding = self.encoding or (
                        os.device_encoding(1) or "utf-8")
                    stdout_val = (
                        completed.stdout.decode(encoding).rstrip("\r\n")
                        if completed.stdout
                        else None
                    )
                    stderr_val = (
                        completed.stderr.decode(encoding).rstrip("\r\n")
                        if completed.stderr
                        else None
                    )
                return {
                    "returncode": completed.returncode,
                    "stdout": stdout_val,
                    "stderr": stderr_val,
                }
            else:
                return None
        finally:
            if stdout_handle:
                stdout_handle.close()
            if stderr_handle and stderr_handle not in (subprocess.STDOUT,):
                stderr_handle.close()


class CmdStep:
    '''A pypyr step to run an executable or command as a subprocess.'''

    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
        self.name = name
        self.context = context
        self.is_shell = is_shell
        self.logger = logging.getLogger(name)
        self.commands: List[Command] = []

        # Parse the step config from context
        cmd_config = context.get("cmd")
        if cmd_config is None:
            raise ValueError("No 'cmd' found in context for CmdStep.")

        self.commands = self._parse_cmd_config(cmd_config)

    def _parse_cmd_config(self, cmd_config: Any) -> List[Command]:
        # Helper to parse the cmd config into a list of Command objects
        commands = []

        def parse_expanded(item: Mapping) -> List[Command]:
            # item is a dict with at least 'run'
            run = item.get("run")
            if run is None:
                raise ValueError("Expanded cmd syntax must have 'run' key.")

            # If run is a list, create a Command for each
            if isinstance(run, list):
                return [
                    Command(
                        run=run_item,
                        save=item.get("save", False),
                        cwd=item.get("cwd"),
                        bytes_=item.get("bytes", False),
                        encoding=item.get("encoding"),
                        stdout=item.get("stdout"),
                        stderr=item.get("stderr"),
                        append=item.get("append", False),
                        is_shell=self.is_shell,
                    )
                    for run_item in run
                ]
            else:
                return [
                    Command(
                        run=run,
                        save=item.get("save", False),
                        cwd=item.get("cwd"),
                        bytes_=item.get("bytes", False),
                        encoding=item.get("encoding"),
                        stdout=item.get("stdout"),
                        stderr=item.get("stderr"),
                        append=item.get("append", False),
                        is_shell=self.is_shell,
                    )
                ]

        # If it's a string, treat as a single command
        if isinstance(cmd_config, str):
            commands.append(
                Command(run=cmd_config, is_shell=self.is_shell)
            )
        # If it's a dict, could be expanded syntax or run as a list
        elif isinstance(cmd_config, dict):
            if "run" in cmd_config:
                commands.extend(parse_expanded(cmd_config))
            else:
                # If dict but not expanded, treat as error
                raise ValueError("Dict cmd config must have 'run' key.")
        # If it's a list, each item can be string or dict
        elif isinstance(cmd_config, list):
            for item in cmd_config:
                if isinstance(item, str):
                    commands.append(
                        Command(run=item, is_shell=self.is_shell)
                    )
                elif isinstance(item, dict):
                    if "run" in item:
                        commands.extend(parse_expanded(item))
                    else:
                        raise ValueError(
                            "Dict cmd config in list must have 'run' key.")
                else:
                    raise ValueError(
                        "List item in cmd config must be str or dict.")
        else:
            raise ValueError("cmd config must be str, dict, or list.")

        return commands

    def create_command(self, cmd_input: Mapping) -> Command:
        '''Create a pypyr.subproc.Command object from expanded step input.'''
        # This method is for a single expanded syntax command
        run = cmd_input.get("run")
        if run is None:
            raise ValueError("Expanded cmd syntax must have 'run' key.")
        return Command(
            run=run,
            save=cmd_input.get("save", False),
            cwd=cmd_input.get("cwd"),
            bytes_=cmd_input.get("bytes", False),
            encoding=cmd_input.get("encoding"),
            stdout=cmd_input.get("stdout"),
            stderr=cmd_input.get("stderr"),
            append=cmd_input.get("append", False),
            is_shell=self.is_shell,
        )

    def run_step(self) -> None:
        '''Spawn a subprocess to run the command or program.
        If cmd.is_save==True, save result of each command to context 'cmdOut'.
        '''
        cmd_outs = []
        for cmd in self.commands:
            self.logger.info(f"Running command: {cmd.run}")
            result = cmd.run_command()
            if cmd.save:
                cmd_outs.append(result)
        # Save to context if any command had save=True
        if cmd_outs:
            # If only one, save as single dict, else as list
            self.context["cmdOut"] = cmd_outs if len(
                cmd_outs) > 1 else cmd_outs[0]
