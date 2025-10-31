
from typing import Mapping, List, Union
from pathlib import Path
import logging
import subprocess
from pypyr.context import Context
from pypyr.subproc import Command


class CmdStep:
    '''A pypyr step to run an executable or command as a subprocess.
    This models a step that takes config like this:
        cmd: <<cmd string>>
    OR, expanded syntax is as a dict
        cmd:
            run: str. mandatory. command + args to execute.
            save: bool. defaults False. save output to cmdOut. Treats output
                as text in the system's encoding and removes newlines at end.
            cwd: str/Pathlike. optional. Working directory for this command.
            bytes (bool): Default False. When `save` return output bytes from
                cmd unaltered, without applying any encoding & text newline
                processing.
            encoding (str): Default None. When `save`, decode cmd output with
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
        cmd:
          run:
            - my-executable --arg
            - cmd here
          save: False
          cwd: ./path/here
    OR, as a list in simplified syntax:
        cmd:
          - my-executable --arg
          - ./another-executable --arg
    Any or all of the list items can use expanded syntax:
        cmd:
          - ./simple-cmd-here --arg1 value
          - run: cmd here
            save: False
            cwd: ./path/here
          - run:
              - my-executable --arg
              - ./another-executable --arg
            save: True cwd: ./path/here
    If save is True, will save the output to context as follows:
        cmdOut:
            returncode: 0
            stdout: 'stdout str here. None if empty.'
            stderr: 'stderr str here. None if empty.'
    If the cmd input contains a list of executables, cmdOut will be a list of
    cmdOut objects, in order executed.
    cmdOut.returncode is the exit status of the called process. Typically 0
    means OK. A negative value -N indicates that the child was terminated by
    signal N (POSIX only).
    The run_step method does the actual work. init parses the input yaml.
    Attributes:
        logger (logger): Logger instantiated by name of calling step.
        context: (pypyr.context.Context): The current pypyr Context.
        commands (list[pypyr.subproc.Command]): Commands to run as subprocess.
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
        self.logger = logging.getLogger(name)
        self.context = context
        self.commands = self.parse_commands(context.get('cmd', []))
        self.is_shell = is_shell
        self.name = name

    def parse_commands(self, cmd_input: Union[str, List, Mapping]) -> List[Command]:
        if isinstance(cmd_input, str):
            return [self.create_command({'run': cmd_input})]
        elif isinstance(cmd_input, list):
            return [self.create_command(item) for item in cmd_input]
        elif isinstance(cmd_input, Mapping):
            return [self.create_command(cmd_input)]
        else:
            raise ValueError("Invalid cmd input type")

    def create_command(self, cmd_input: Mapping) -> Command:
        '''Create a pypyr.subproc.Command object from expanded step input.'''
        run = cmd_input.get('run', [])
        if isinstance(run, str):
            run = [run]
        elif not isinstance(run, list):
            raise ValueError("run must be a string or a list of strings")

        save = cmd_input.get('save', False)
        cwd = cmd_input.get('cwd', None)
        bytes_ = cmd_input.get('bytes', False)
        encoding = cmd_input.get('encoding', None)
        stdout = cmd_input.get('stdout', None)
        stderr = cmd_input.get('stderr', None)
        append = cmd_input.get('append', False)

        return Command(
            run=run,
            save=save,
            cwd=cwd,
            bytes_=bytes_,
            encoding=encoding,
            stdout=stdout,
            stderr=stderr,
            append=append
        )

    def run_step(self) -> None:
        '''Spawn a subprocess to run the command or program.
        If cmd.is_save==True, save result of each command to context 'cmdOut'.
        '''
        results = []
        for command in self.commands:
            self.logger.info(f"Running command: {command.run}")
            result = command.run(is_shell=self.is_shell)
            if command.save:
                results.append({
                    'returncode': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                })
            if result.returncode != 0:
                self.logger.error(
                    f"Command failed with return code {result.returncode}: {command.run}")
            else:
                self.logger.info(f"Command succeeded: {command.run}")

        if results:
            self.context['cmdOut'] = results if len(
                results) > 1 else results[0]
