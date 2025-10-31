
import asyncio
import logging
from typing import Any, Mapping, List, Union
from pathlib import Path

# Dummy stubs for pypyr classes (replace with actual imports in real usage)


class Context(dict):
    pass


class SubprocessResult:
    def __init__(self, cmd, returncode, stdout, stderr):
        self.cmd = cmd
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class Command:
    def __init__(
        self,
        run: Union[str, List[str]],
        save: bool = False,
        cwd: Union[str, Path, None] = None,
        bytes_: bool = False,
        encoding: str = None,
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


class Commands:
    def __init__(self, commands: List[Command]):
        self.commands = commands

# Actual implementation


class AsyncCmdStep:
    '''A pypyr step to run executables/commands concurrently as a subprocess.'''

    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
        self.name = name
        self.context = context
        self.is_shell = is_shell
        self.logger = logging.getLogger(name)
        self.commands = self._parse_commands()

    def _parse_commands(self) -> Commands:
        cmds = self.context.get("cmds")
        if cmds is None:
            raise ValueError("No 'cmds' found in context for AsyncCmdStep.")

        commands = []
        if isinstance(cmds, dict):
            # Expanded syntax, single dict
            commands.extend(self._parse_cmds_dict(cmds))
        elif isinstance(cmds, list):
            for item in cmds:
                if isinstance(item, dict):
                    commands.extend(self._parse_cmds_dict(item))
                elif isinstance(item, list):
                    # Serial group: each item is a string or dict
                    serial_cmds = []
                    for subitem in item:
                        if isinstance(subitem, dict):
                            serial_cmds.extend(self._parse_cmds_dict(subitem))
                        else:
                            serial_cmds.append(
                                Command(run=subitem)
                            )
                    commands.append(serial_cmds)
                else:
                    commands.append(Command(run=item))
        else:
            # Single string
            commands.append(Command(run=cmds))
        # Flatten serial groups into single-level list, but keep serial groups as lists
        flat_commands = []
        for cmd in commands:
            if isinstance(cmd, list):
                flat_commands.append(cmd)
            else:
                flat_commands.append([cmd])
        return Commands(flat_commands)

    def _parse_cmds_dict(self, cmds_dict: Mapping) -> List[Command]:
        # If 'run' is not present, treat the dict as a single command
        if "run" not in cmds_dict:
            return [self.create_command(cmds_dict)]
        run = cmds_dict["run"]
        # If run is a list, each item is a command (or serial group)
        if isinstance(run, list):
            commands = []
            for item in run:
                if isinstance(item, list):
                    # Serial group
                    serial_cmds = []
                    for subitem in item:
                        if isinstance(subitem, dict):
                            serial_cmds.append(self.create_command(
                                {**cmds_dict, **subitem}))
                        else:
                            serial_cmds.append(self.create_command(
                                {**cmds_dict, "run": subitem}))
                    commands.append(serial_cmds)
                elif isinstance(item, dict):
                    commands.append(self.create_command({**cmds_dict, **item}))
                else:
                    commands.append(self.create_command(
                        {**cmds_dict, "run": item}))
            return commands
        else:
            return [self.create_command(cmds_dict)]

    def create_command(self, cmd_input: Mapping) -> Command:
        run = cmd_input.get("run")
        save = cmd_input.get("save", False)
        cwd = cmd_input.get("cwd")
        bytes_ = cmd_input.get("bytes", False)
        encoding = cmd_input.get("encoding")
        stdout = cmd_input.get("stdout")
        stderr = cmd_input.get("stderr")
        append = cmd_input.get("append", False)
        return Command(
            run=run,
            save=save,
            cwd=cwd,
            bytes_=bytes_,
            encoding=encoding,
            stdout=stdout,
            stderr=stderr,
            append=append,
        )

    async def _run_command(
        self, command: Command, is_shell: bool
    ) -> SubprocessResult:
        # Prepare command and shell
        cmd = command.run
        shell = is_shell
        if isinstance(cmd, str):
            args = cmd if shell else cmd.split()
        else:
            args = cmd

        # Prepare stdout/stderr
        stdout_file = None
        stderr_file = None
        stdout = asyncio.subprocess.PIPE
        stderr = asyncio.subprocess.PIPE

        def get_file_handle(path, append):
            mode = "ab" if command.bytes else "a" if append else "w"
            if path == "/dev/null":
                return open(Path("/dev/null"), mode)
            return open(Path(path), mode)

        if command.stdout:
            if command.stdout == "/dev/null":
                stdout_file = get_file_handle(command.stdout, command.append)
                stdout = stdout_file
            else:
                stdout_file = get_file_handle(command.stdout, command.append)
                stdout = stdout_file
        if command.stderr:
            if command.stderr == "/dev/null":
                stderr_file = get_file_handle(command.stderr, command.append)
                stderr = stderr_file
            elif command.stderr == "/dev/stdout":
                stderr = asyncio.subprocess.STDOUT
            else:
                stderr_file = get_file_handle(command.stderr, command.append)
                stderr = stderr_file

        try:
            proc = await asyncio.create_subprocess_exec(
                *args if not shell else [],
                args if shell else None,
                shell=shell,
                cwd=command.cwd,
                stdout=stdout,
                stderr=stderr,
            )
            out, err = await proc.communicate()
            if stdout_file:
                stdout_file.close()
                out = None
            if stderr_file:
                stderr_file.close()
                err = None
            if command.save:
                if command.bytes:
                    result_out = out
                    result_err = err
                else:
                    enc = command.encoding or "utf-8"
                    result_out = out.decode(enc).rstrip("\n") if out else None
                    result_err = err.decode(enc).rstrip("\n") if err else None
            else:
                result_out = None
                result_err = None
            return SubprocessResult(
                cmd=args, returncode=proc.returncode, stdout=result_out, stderr=result_err
            )
        except Exception as ex:
            return ex

    async def _run_serial(self, commands: List[Command], is_shell: bool) -> List[Any]:
        results = []
        for cmd in commands:
            result = await self._run_command(cmd, is_shell)
            results.append(result)
        return results

    async def _run_all(self):
        # self.commands.commands is a list of lists (serial groups)
        tasks = []
        for serial_group in self.commands.commands:
            if len(serial_group) == 1:
                # Single command, run concurrently
                tasks.append(self._run_command(serial_group[0], self.is_shell))
            else:
                # Serial group, run in order
                tasks.append(self._run_serial(serial_group, self.is_shell))
        results = await asyncio.gather(*tasks)
        # Flatten serial group results
        flat_results = []
        for res in results:
            if isinstance(res, list):
                flat_results.extend(res)
            else:
                flat_results.append(res)
        return flat_results

    def run_step(self) -> None:
        '''Spawn subprocesses to run the commands asynchronously.'''
        results = asyncio.run(self._run_all())
        # Save to context if any command has save=True
        if any(
            cmd.save
            for group in self.commands.commands
            for cmd in group
        ):
            self.context["cmdOut"] = results
