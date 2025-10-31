
import logging
import os
from pathlib import Path
from typing import Mapping, List, Union, Optional, Dict, Any
from pypyr.context import Context
from pypyr.subproc import Command


class CmdStep:
    '''A pypyr step to run an executable or command as a subprocess.'''

    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
        '''Initialize the CmdStep.'''
        self.logger = logging.getLogger(name)
        self.context = context
        self.is_shell = is_shell
        self.name = name
        self.commands: List[Command] = []

        cmd_config = context.get('cmd')
        if cmd_config is None:
            raise KeyError("cmd not found in context.")

        if isinstance(cmd_config, str):
            self.commands.append(self.create_command({'run': cmd_config}))
        elif isinstance(cmd_config, list):
            for cmd_item in cmd_config:
                if isinstance(cmd_item, str):
                    self.commands.append(
                        self.create_command({'run': cmd_item}))
                else:
                    self.commands.append(self.create_command(cmd_item))
        elif isinstance(cmd_config, dict):
            if 'run' in cmd_config:
                self.commands.append(self.create_command(cmd_config))
            else:
                raise KeyError("cmd must have 'run' key in expanded syntax.")
        else:
            raise TypeError("cmd must be str, list, or dict.")

    def create_command(self, cmd_input: Mapping) -> Command:
        '''Create a pypyr.subproc.Command object from expanded step input.'''
        run = cmd_input.get('run')
        if run is None:
            raise KeyError("cmd must have 'run' key in expanded syntax.")

        save = cmd_input.get('save', False)
        cwd = cmd_input.get('cwd')
        if cwd is not None:
            cwd = Path(cwd)

        bytes_output = cmd_input.get('bytes', False)
        encoding = cmd_input.get('encoding')
        stdout = cmd_input.get('stdout')
        stderr = cmd_input.get('stderr')
        append = cmd_input.get('append', False)

        if isinstance(run, str):
            return Command(
                cmd=run,
                is_shell=self.is_shell,
                save=save,
                cwd=cwd,
                bytes_output=bytes_output,
                encoding=encoding,
                stdout=stdout,
                stderr=stderr,
                append=append
            )
        elif isinstance(run, list):
            return Command(
                cmd=run,
                is_shell=self.is_shell,
                save=save,
                cwd=cwd,
                bytes_output=bytes_output,
                encoding=encoding,
                stdout=stdout,
                stderr=stderr,
                append=append
            )
        else:
            raise TypeError("'run' must be str or list.")

    def run_step(self) -> None:
        '''Spawn a subprocess to run the command or program.'''
        if not self.commands:
            return

        cmd_out = []
        for cmd in self.commands:
            result = cmd.run()
            if cmd.save:
                cmd_out.append({
                    'returncode': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                })

        if any(cmd.save for cmd in self.commands):
            if len(cmd_out) == 1:
                self.context['cmdOut'] = cmd_out[0]
            else:
                self.context['cmdOut'] = cmd_out
