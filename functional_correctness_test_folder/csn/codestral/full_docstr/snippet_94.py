
import logging
from pathlib import Path
from typing import Mapping, List, Union

from pypyr.context import Context
from pypyr.subproc import Command


class CmdStep:
    '''A pypyr step to run an executable or command as a subprocess.'''

    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
        '''Initialize the CmdStep.'''
        self.logger = logging.getLogger(__name__)
        self.context = context
        self.is_shell = is_shell
        self.name = name

        cmd_input = context.get_formatted('cmd')

        if isinstance(cmd_input, str):
            self.commands = [Command(cmd_input, is_shell=is_shell)]
        elif isinstance(cmd_input, list):
            self.commands = []
            for item in cmd_input:
                if isinstance(item, str):
                    self.commands.append(Command(item, is_shell=is_shell))
                elif isinstance(item, dict):
                    self.commands.append(self.create_command(item))
        elif isinstance(cmd_input, dict):
            self.commands = [self.create_command(cmd_input)]
        else:
            raise ValueError(f"Invalid cmd input type: {type(cmd_input)}")

    def create_command(self, cmd_input: Mapping) -> Command:
        '''Create a pypyr.subproc.Command object from expanded step input.'''
        run_input = cmd_input.get('run')
        if isinstance(run_input, str):
            command = Command(run_input, is_shell=self.is_shell)
        elif isinstance(run_input, list):
            command = Command(run_input, is_shell=self.is_shell)
        else:
            raise ValueError(f"Invalid run input type: {type(run_input)}")

        command.is_save = cmd_input.get('save', False)
        command.cwd = cmd_input.get('cwd')
        command.bytes = cmd_input.get('bytes', False)
        command.encoding = cmd_input.get('encoding')
        command.stdout = cmd_input.get('stdout')
        command.stderr = cmd_input.get('stderr')
        command.append = cmd_input.get('append', False)

        return command

    def run_step(self) -> None:
        '''Spawn a subprocess to run the command or program.'''
        cmd_out_list = []

        for command in self.commands:
            cmd_out = command.run()

            if command.is_save:
                cmd_out_list.append({
                    'returncode': cmd_out.returncode,
                    'stdout': cmd_out.stdout,
                    'stderr': cmd_out.stderr
                })

        if cmd_out_list:
            if len(cmd_out_list) == 1:
                self.context['cmdOut'] = cmd_out_list[0]
            else:
                self.context['cmdOut'] = cmd_out_list
