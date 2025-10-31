
import logging
from pathlib import Path
from typing import Mapping, List, Union, Optional
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
            self.commands = [Command(cmd_input)]
        elif isinstance(cmd_input, list):
            self.commands = []
            for cmd in cmd_input:
                if isinstance(cmd, str):
                    self.commands.append(Command(cmd))
                elif isinstance(cmd, dict):
                    self.commands.append(self.create_command(cmd))
        elif isinstance(cmd_input, dict):
            self.commands = [self.create_command(cmd_input)]
        else:
            raise ValueError(f"Invalid cmd input type: {type(cmd_input)}")

    def create_command(self, cmd_input: Mapping) -> Command:
        '''Create a pypyr.subproc.Command object from expanded step input.'''
        run_input = cmd_input.get('run')
        if isinstance(run_input, str):
            run = run_input
        elif isinstance(run_input, list):
            run = ' && '.join(run_input)
        else:
            raise ValueError(f"Invalid run input type: {type(run_input)}")

        save = cmd_input.get('save', False)
        cwd = cmd_input.get('cwd')
        if cwd is not None:
            cwd = Path(cwd)

        bytes_output = cmd_input.get('bytes', False)
        encoding = cmd_input.get('encoding')

        stdout = cmd_input.get('stdout')
        if stdout is not None:
            stdout = Path(stdout) if stdout != '/dev/null' else '/dev/null'

        stderr = cmd_input.get('stderr')
        if stderr is not None:
            stderr = Path(stderr) if stderr not in (
                '/dev/null', '/dev/stdout') else stderr

        append = cmd_input.get('append', False)

        return Command(
            run=run,
            save=save,
            cwd=cwd,
            bytes=bytes_output,
            encoding=encoding,
            stdout=stdout,
            stderr=stderr,
            append=append
        )

    def run_step(self) -> None:
        '''Spawn a subprocess to run the command or program.'''
        cmd_outs = []
        for cmd in self.commands:
            cmd_out = cmd.run(self.is_shell)
            if cmd.save:
                cmd_outs.append(cmd_out)

        if cmd_outs:
            if len(cmd_outs) == 1:
                self.context['cmdOut'] = cmd_outs[0]
            else:
                self.context['cmdOut'] = cmd_outs
