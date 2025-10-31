
import asyncio
from pathlib import Path
from typing import Mapping, List, Union, Optional, Dict, Any
from pypyr.context import Context
from pypyr.subproc import Command, Commands, SubprocessResult
import logging
import os


class AsyncCmdStep:
    '''A pypyr step to run executables/commands concurrently as a subprocess.'''

    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
        '''Initialize the CmdStep.'''
        self.logger = logging.getLogger(name)
        self.context = context
        self.is_shell = is_shell
        self.name = name
        self.commands = self._parse_commands(context)

    def _parse_commands(self, context: Context) -> Commands:
        '''Parse the commands from the context.'''
        cmds_config = context.get('cmds')
        if not cmds_config:
            raise ValueError("cmds not found in context.")

        commands = Commands()

        if isinstance(cmds_config, (str, list)):
            self._parse_simple_commands(cmds_config, commands)
        elif isinstance(cmds_config, dict):
            self._parse_expanded_commands(cmds_config, commands)
        else:
            raise ValueError("cmds must be a string, list, or dict.")

        return commands

    def _parse_simple_commands(self, cmds_config: Union[str, List], commands: Commands) -> None:
        '''Parse simple command syntax.'''
        if isinstance(cmds_config, str):
            cmds_config = [cmds_config]

        for cmd in cmds_config:
            if isinstance(cmd, (str, list)):
                if isinstance(cmd, list):
                    sub_commands = []
                    for sub_cmd in cmd:
                        sub_commands.append(
                            self.create_command({'run': sub_cmd}))
                    commands.add_serial(*sub_commands)
                else:
                    commands.add_parallel(self.create_command({'run': cmd}))
            elif isinstance(cmd, dict):
                self._parse_expanded_commands(cmd, commands)
            else:
                raise ValueError(f"Invalid command format: {cmd}")

    def _parse_expanded_commands(self, cmds_config: Dict, commands: Commands) -> None:
        '''Parse expanded command syntax.'''
        run = cmds_config.get('run')
        if not run:
            raise ValueError("'run' is required in expanded command syntax.")

        save = cmds_config.get('save', False)
        cwd = cmds_config.get('cwd')
        bytes_output = cmds_config.get('bytes', False)
        encoding = cmds_config.get('encoding')
        stdout = cmds_config.get('stdout')
        stderr = cmds_config.get('stderr')
        append = cmds_config.get('append', False)

        cmd_kwargs = {
            'save': save,
            'cwd': str(Path(cwd).resolve()) if cwd else None,
            'bytes': bytes_output,
            'encoding': encoding,
            'stdout': stdout,
            'stderr': stderr,
            'append': append,
        }

        if isinstance(run, str):
            cmd_kwargs['run'] = run
            commands.add_parallel(self.create_command(cmd_kwargs))
        elif isinstance(run, list):
            for cmd in run:
                if isinstance(cmd, str):
                    cmd_kwargs['run'] = cmd
                    commands.add_parallel(self.create_command(cmd_kwargs))
                elif isinstance(cmd, list):
                    sub_commands = []
                    for sub_cmd in cmd:
                        sub_cmd_kwargs = cmd_kwargs.copy()
                        sub_cmd_kwargs['run'] = sub_cmd
                        sub_commands.append(
                            self.create_command(sub_cmd_kwargs))
                    commands.add_serial(*sub_commands)
                else:
                    raise ValueError(f"Invalid command format in 'run': {cmd}")
        else:
            raise ValueError("'run' must be a string or list.")

    def create_command(self, cmd_input: Mapping) -> Command:
        '''Create pypyr.aio.subproc.Command object from expanded step input.'''
        run = cmd_input.get('run')
        if not run:
            raise ValueError("'run' is required in command input.")

        save = cmd_input.get('save', False)
        cwd = cmd_input.get('cwd')
        bytes_output = cmd_input.get('bytes', False)
        encoding = cmd_input.get('encoding')
        stdout = cmd_input.get('stdout')
        stderr = cmd_input.get('stderr')
        append = cmd_input.get('append', False)

        return Command(
            cmd=run,
            is_shell=self.is_shell,
            cwd=cwd,
            save=save,
            bytes_output=bytes_output,
            encoding=encoding,
            stdout=stdout,
            stderr=stderr,
            append=append,
        )

    async def run_step(self) -> None:
        '''Spawn subprocesses to run the commands asynchronously.'''
        results = await self.commands.run()
        if any(cmd.save for cmd in self.commands.all_commands):
            self.context['cmdOut'] = results
