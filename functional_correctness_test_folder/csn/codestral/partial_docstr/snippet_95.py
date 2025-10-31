
import asyncio
from pathlib import Path
from typing import Mapping, Union, List, Optional, Any
from pypyr.context import Context
from pypyr.subproc import Commands, Command, SubprocessResult
from pypyr.errors import KeyNotInContextError


class AsyncCmdStep:
    '''A pypyr step to run executables/commands concurrently as a subprocess.
    This models a step that takes config like this in simple syntax:
        cmds:
            - <<cmd string 1>>
            - <<cmd string 2>>
    All the commands will run concurrently, in parallel.
    OR, expanded syntax is as a dict
        cmds:
            run: list[str | list[str]]. mandatory. command + args to execute.
                If list entry is another list[str], the sub-list will run in
                serial.
            save: bool. defaults False. save output to cmdOut. Treats output
                as text in the system's encoding and removes newlines at end.
            cwd: str/Pathlike. optional. Working directory for these commands.
            bytes (bool): Default False. When `save` return output bytes from
                cmds unaltered, without applying any encoding & text newline
                processing.
            encoding (str): Default None. When `save`, decode output with
                this encoding. The default of None uses the system encoding and
                should "just work".
            stdout (str | Path): Default None. Write stdout to this file path.
                Special value `/dev/null` writes to the system null device.
            stderr (str | Path): Default None. Write stderr to this file path.
                Special value `/dev/null` writes to the system null device.
                Special value `/dev/stdout` redirects err output to stdout.
            append (bool): Default False. When stdout/stderr a file, append
                rather than overwrite. Default is to overwrite.
    In expanded syntax, `run` can be a simple string or a list:
        cmds:
          run:
            - ./my-executable --arg
            - [./another-executable --arg, ./arb-executable arghere]
          save: False
          cwd: ./path/here
    As a list in simplified syntax:
        cmds:
          - my-executable --arg
          - ./another-executable --arg
    Any or all of the list items can use expanded syntax:
        cmds:
          - ./simple-cmd-here --arg1 value
          - run: cmd here
            save: False cwd: ./path/here
          - run:
              - my-executable --arg
              - ./another-executable --arg
            save: True
            cwd: ./path/here
    Any of the list items can in turn be a list. A sub-list will run in serial.
    In this example A, B.1 & C will start concurrently. B.2 will only run once
    B.1 is finished.
        cmds:
            - A
            - [B.1, B.2]
            - C
    If save is True, will save the output to context as cmdOut.
    cmdOut will be a list of pypyr.subproc.SubprocessResult objects, in order
    executed.
    SubprocessResult has the following properties:
    cmd: the cmd/args executed
    returncode: 0
    stdout: 'stdout str here. None if empty.'
    stderr: 'stderr str here. None if empty.'
    cmdOut.returncode is the exit status of the called process. Typically 0
    means OK. A negative value -N indicates that the child was terminated by
    signal N (POSIX only).
    The run_step method does the actual work. init parses the input yaml.
    Attributes:
        logger (logger): Logger instantiated by name of calling step.
        context: (pypyr.context.Context): The current pypyr Context.
        commands (pypyr.subproc.Commands): Commands to run as subprocess.
        is_shell (bool): True if subprocess should run through default shell.
        name (str): Name of calling step. Used for logging output & error
            messages.
    '''

    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
        '''Initialize the CmdStep.
        The step config in the context dict in simplified syntax:
            cmd: <<cmd string>>
        OR, as a dict in expanded syntax:
            cmd:
                run: str. mandatory. command + args to execute.
                save: bool. optional. defaults False. save output to cmdOut.
                cwd: str/path. optional. if specified, change the working
                     directory just for the duration of the command.
        `run` can be a single string, or it can be a list of string if there
        are multiple commands to execute with the same settings.
        OR, as a list:
            cmd:
                - my-executable --arg
                - ./another-executable --arg
        Any or all of the list items can be in expanded syntax.
        Args:
            name (str): Unique name for step. Likely __name__ of calling step.
            context (pypyr.context.Context): Look for step config in this
                context instance.
            is_shell (bool): Set to true to execute cmd through the default
                shell.
        '''
        self.logger = context.logger
        self.context = context
        self.is_shell = is_shell
        self.name = name

        try:
            cmds_input = context.get_formatted('cmds')
        except KeyNotInContextError as e:
            raise KeyNotInContextError(
                f"cmds key not found in context. {e}") from e

        self.commands = Commands()

        if isinstance(cmds_input, list):
            for cmd_input in cmds_input:
                if isinstance(cmd_input, list):
                    for sub_cmd_input in cmd_input:
                        if isinstance(sub_cmd_input, str):
                            self.commands.append(
                                Command(
                                    run=sub_cmd_input,
                                    is_shell=is_shell
                                )
                            )
                        elif isinstance(sub_cmd_input, dict):
                            self.commands.append(
                                self.create_command(sub_cmd_input)
                            )
                elif isinstance(cmd_input, str):
                    self.commands.append(
                        Command(
                            run=cmd_input,
                            is_shell=is_shell
                        )
                    )
                elif isinstance(cmd_input, dict):
                    self.commands.append(
                        self.create_command(cmd_input)
                    )
        elif isinstance(cmds_input, dict):
            self.commands.append(
                self.create_command(cmds_input)
            )

    def create_command(self, cmd_input: Mapping) -> Command:
        '''Create pypyr.aio.subproc.Command object from expanded step input.'''
        run = cmd_input.get('run')
        if not run:
            raise KeyNotInContextError(
                f"run key not found in cmd input. {cmd_input}")

        save = cmd_input.get('save', False)
        cwd = cmd_input.get('cwd')
        if cwd:
            cwd = Path(cwd)

        bytes_output = cmd_input.get('bytes', False)
        encoding = cmd_input.get('encoding')

        stdout = cmd_input.get('stdout')
        if stdout:
            stdout = Path(stdout) if stdout != '/dev/null' else stdout

        stderr = cmd_input.get('stderr')
        if stderr:
            stderr = Path(stderr) if stderr not in (
                '/dev/null', '/dev/stdout') else stderr

        append = cmd_input.get('append', False)

        return Command(
            run=run,
            is_shell=self.is_shell,
            is_save=save,
            cwd=cwd,
            bytes_output=bytes_output,
            encoding=encoding,
            stdout=stdout,
            stderr=stderr,
            append=append
        )

    def run_step(self) -> None:
        '''Spawn subprocesses to run the commands asynchronously.
        If cmd.is_save==True, save aggregate result of all commands to context
        'cmdOut'.
        cmdOut will be a list of pypyr.subproc.SubprocessResult or Exception
        objects, in order executed.
        SubprocessResult has the following properties:
        cmd: the cmd/args executed
        returncode: 0
        stdout: 'stdout str here. None if empty.'
        stderr: 'stderr str here. None if empty.'
        '''
        async def run_commands():
            tasks = []
            for cmd in self.commands:
                if isinstance(cmd.run, list):
                    for sub_cmd in cmd.run:
                        if isinstance(sub_cmd, list):
                            for sub_sub_cmd in sub_cmd:
                                tasks.append(
                                    asyncio.create_task(sub_sub_cmd.run()))
                        else:
                            tasks.append(asyncio.create_task(sub_cmd.run()))
                else:
                    tasks.append(asyncio.create_task(cmd.run()))

            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(run_commands())

        if any(cmd.is_save for cmd in self.commands):
            self.context['cmdOut'] = results
