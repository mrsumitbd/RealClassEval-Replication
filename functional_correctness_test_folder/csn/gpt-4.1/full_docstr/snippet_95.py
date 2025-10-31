
import asyncio
import logging
from pathlib import Path
from typing import Any, Mapping, List, Union, Optional

# Dummy stubs for pypyr classes, replace with actual imports in real usage


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
        run: Union[str, List[Union[str, List[str]]]],
        save: bool = False,
        cwd: Optional[Union[str, Path]] = None,
        bytes_: bool = False,
        encoding: Optional[str] = None,
        stdout: Optional[Union[str, Path]] = None,
        stderr: Optional[Union[str, Path]] = None,
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


def _is_expanded_cmd(item):
    return isinstance(item, dict) and "run" in item


def _normalize_cmds(cmds):
    # Accepts string, list, or dict, returns list of dicts (expanded syntax)
    if isinstance(cmds, str):
        return [{"run": cmds}]
    elif isinstance(cmds, dict):
        # Single expanded syntax
        return [cmds]
    elif isinstance(cmds, list):
        result = []
        for item in cmds:
            if _is_expanded_cmd(item):
                result.append(item)
            elif isinstance(item, list):
                # Serial group
                result.append({"run": item})
            else:
                # Simple string
                result.append({"run": item})
        return result
    else:
        raise ValueError("Invalid cmds format")


def _to_list_of_str(cmd):
    if isinstance(cmd, str):
        return [cmd]
    elif isinstance(cmd, list):
        return cmd
    else:
        raise ValueError("Invalid command type")


def _get_null_device():
    import os
    return os.devnull


async def _run_subprocess(
    cmd: Union[str, List[str]],
    shell: bool,
    cwd: Optional[Union[str, Path]],
    save: bool,
    bytes_: bool,
    encoding: Optional[str],
    stdout_path: Optional[Union[str, Path]],
    stderr_path: Optional[Union[str, Path]],
    append: bool,
    logger: logging.Logger,
):
    # Prepare stdout/stderr
    stdout = None
    stderr = None
    stdout_file = None
    stderr_file = None
    try:
        if stdout_path:
            if stdout_path == "/dev/null":
                stdout = open(_get_null_device(), "ab" if append else "wb")
                stdout_file = stdout
            else:
                mode = "ab" if append else "wb"
                stdout = open(stdout_path, mode)
                stdout_file = stdout
        if stderr_path:
            if stderr_path == "/dev/null":
                stderr = open(_get_null_device(), "ab" if append else "wb")
                stderr_file = stderr
            elif stderr_path == "/dev/stdout":
                stderr = asyncio.subprocess.STDOUT
            else:
                mode = "ab" if append else "wb"
                stderr = open(stderr_path, mode)
                stderr_file = stderr

        proc = await asyncio.create_subprocess_shell(
            cmd if isinstance(cmd, str) else " ".join(cmd),
            cwd=str(cwd) if cwd else None,
            stdout=stdout if stdout else asyncio.subprocess.PIPE,
            stderr=stderr if stderr else asyncio.subprocess.PIPE,
        ) if shell else await asyncio.create_subprocess_exec(
            *(cmd if isinstance(cmd, list) else cmd.split()),
            cwd=str(cwd) if cwd else None,
            stdout=stdout if stdout else asyncio.subprocess.PIPE,
            stderr=stderr if stderr else asyncio.subprocess.PIPE,
        )

        out, err = await proc.communicate()
        returncode = proc.returncode

        # If output is redirected to file, set to None
        if stdout_file:
            out = None
        if stderr_file or stderr_path == "/dev/stdout":
            err = None

        if save:
            if bytes_:
                result_out = out
                result_err = err
            else:
                enc = encoding or (out and getattr(
                    out, "encoding", None)) or "utf-8"
                result_out = out.decode(enc).rstrip(
                    "\r\n") if out is not None else None
                result_err = err.decode(enc).rstrip(
                    "\r\n") if err is not None else None
        else:
            result_out = None
            result_err = None

        return SubprocessResult(
            cmd=cmd,
            returncode=returncode,
            stdout=result_out,
            stderr=result_err,
        )
    finally:
        if stdout_file:
            stdout_file.close()
        if stderr_file:
            stderr_file.close()


async def _run_serial(
    cmds: List[Union[str, List[str]]],
    shell: bool,
    cwd: Optional[Union[str, Path]],
    save: bool,
    bytes_: bool,
    encoding: Optional[str],
    stdout: Optional[Union[str, Path]],
    stderr: Optional[Union[str, Path]],
    append: bool,
    logger: logging.Logger,
):
    results = []
    for cmd in cmds:
        res = await _run_subprocess(
            cmd,
            shell,
            cwd,
            save,
            bytes_,
            encoding,
            stdout,
            stderr,
            append,
            logger,
        )
        results.append(res)
    return results


async def _run_command(
    command: Command,
    shell: bool,
    logger: logging.Logger,
):
    run = command.run
    if isinstance(run, list):
        # Serial group
        return await _run_serial(
            run,
            shell,
            command.cwd,
            command.save,
            command.bytes,
            command.encoding,
            command.stdout,
            command.stderr,
            command.append,
            logger,
        )
    else:
        # Single command
        return [
            await _run_subprocess(
                run,
                shell,
                command.cwd,
                command.save,
                command.bytes,
                command.encoding,
                command.stdout,
                command.stderr,
                command.append,
                logger,
            )
        ]


class AsyncCmdStep:
    '''A pypyr step to run executables/commands concurrently as a subprocess.'''

    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
        self.name = name
        self.context = context
        self.is_shell = is_shell
        self.logger = logging.getLogger(name)
        # Parse config
        cmds_config = context.get("cmds")
        if cmds_config is None:
            raise ValueError("No 'cmds' found in context for AsyncCmdStep")
        # Normalize to list of expanded dicts
        cmds_list = _normalize_cmds(cmds_config)
        self.commands = Commands([self.create_command(cmd)
                                 for cmd in cmds_list])

    def create_command(self, cmd_input: Mapping) -> Command:
        # Accepts expanded syntax dict, returns Command
        run = cmd_input.get("run")
        save = cmd_input.get("save", False)
        cwd = cmd_input.get("cwd", None)
        bytes_ = cmd_input.get("bytes", False)
        encoding = cmd_input.get("encoding", None)
        stdout = cmd_input.get("stdout", None)
        stderr = cmd_input.get("stderr", None)
        append = cmd_input.get("append", False)
        # If run is a list, flatten any sublists to serial groups
        if isinstance(run, list):
            # Each item can be a string or a list (serial group)
            run_list = []
            for item in run:
                if isinstance(item, list):
                    # Serial group
                    run_list.extend(item)
                else:
                    run_list.append(item)
            run = run_list
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

    def run_step(self) -> None:
        async def _run_all():
            tasks = []
            for command in self.commands.commands:
                tasks.append(_run_command(command, self.is_shell, self.logger))
            # Run all commands concurrently
            all_results = await asyncio.gather(*tasks, return_exceptions=True)
            # Flatten results (serial groups are lists)
            flat_results = []
            for res in all_results:
                if isinstance(res, list):
                    flat_results.extend(res)
                else:
                    flat_results.append(res)
            # Save to context if any command has save=True
            if any(cmd.save for cmd in self.commands.commands):
                self.context["cmdOut"] = flat_results

        asyncio.run(_run_all())
