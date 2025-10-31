
import asyncio
import logging
from pathlib import Path
from typing import Mapping, Union, List, Optional

from pypyr.context import Context
from pypyr.subproc import Commands, Command, SubprocessResult


class AsyncCmdStep:
    '''A pypyr step to run executables/commands concurrently as a subprocess.'''

    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
        '''Initialize the CmdStep.'''
        self.logger = logging.getLogger(__name__)
        self.context = context
        self.is_shell = is_shell
        self.name = name

        step_dict = context.get_formatted(name)
        self.commands = Commands()

        if isinstance(step_dict, list):
            for cmd_input in step_dict:
                if isinstance(cmd_input, list):
                    for sub_cmd_input in cmd_input:
                        if isinstance(sub_cmd_input, dict):
                            self.commands.append(
                                self.create_command(sub_cmd_input))
                        else:
                            self.commands.append(Command(sub_cmd_input))
                elif isinstance(cmd_input, dict):
                    self.commands.append(self.create_command(cmd_input))
                else:
                    self.commands.append(Command(cmd_input))
        elif isinstance(step_dict, dict):
            self.commands.append(self.create_command(step_dict))
        else:
            self.commands.append(Command(step_dict))

    def create_command(self, cmd_input: Mapping) -> Command:
        '''Create pypyr.aio.subproc.Command object from expanded step input.'''
        run = cmd_input.get('run')
        save = cmd_input.get('save', False)
        cwd = cmd_input.get('cwd')
        bytes_output = cmd_input.get('bytes', False)
        encoding = cmd_input.get('encoding')
        stdout = cmd_input.get('stdout')
        stderr = cmd_input.get('stderr')
        append = cmd_input.get('append', False)

        if isinstance(run, list):
            cmd = Command(run, save=save, cwd=cwd, bytes=bytes_output,
                          encoding=encoding, stdout=stdout, stderr=stderr, append=append)
        else:
            cmd = Command(run, save=save, cwd=cwd, bytes=bytes_output,
                          encoding=encoding, stdout=stdout, stderr=stderr, append=append)

        return cmd

    async def run_step(self) -> None:
        '''Spawn subprocesses to run the commands asynchronously.'''
        results = await self.commands.run(self.is_shell)

        if any(cmd.is_save for cmd in self.commands):
            self.context['cmdOut'] = results
