
import asyncio
from pathlib import Path
from typing import Mapping, List, Union, Optional, Dict, Any
from pypyr.context import Context
from pypyr.subproc import Command, Commands, SubprocessResult


class AsyncCmdStep:
    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
        self.logger = None  # Initialize logger as per your logging setup
        self.context = context
        self.is_shell = is_shell
        self.name = name
        self.commands = self._parse_commands(context)

    def _parse_commands(self, context: Context) -> Commands:
        cmds_config = context.get('cmds')
        if not cmds_config:
            raise ValueError("No 'cmds' found in context.")

        commands = Commands()

        if isinstance(cmds_config, (str, list)):
            self._parse_simple_commands(cmds_config, commands)
        elif isinstance(cmds_config, dict):
            self._parse_expanded_commands(cmds_config, commands)
        else:
            raise ValueError(
                "Invalid 'cmds' format. Must be str, list, or dict.")

        return commands

    def _parse_simple_commands(self, cmds_config: Union[str, List], commands: Commands) -> None:
        if isinstance(cmds_config, str):
            commands.add(Command(run=[cmds_config]))
        else:
            for cmd in cmds_config:
                if isinstance(cmd, (str, list)):
                    commands.add(
                        Command(run=[cmd] if isinstance(cmd, str) else cmd))
                elif isinstance(cmd, dict):
                    self._parse_expanded_commands(cmd, commands)
                else:
                    raise ValueError("Invalid command format in list.")

    def _parse_expanded_commands(self, cmds_config: Dict, commands: Commands) -> None:
        if 'run' not in cmds_config:
            raise ValueError("'run' is mandatory in expanded command syntax.")

        run = cmds_config['run']
        save = cmds_config.get('save', False)
        cwd = cmds_config.get('cwd')
        bytes_output = cmds_config.get('bytes', False)
        encoding = cmds_config.get('encoding')
        stdout = cmds_config.get('stdout')
        stderr = cmds_config.get('stderr')
        append = cmds_config.get('append', False)

        if isinstance(run, str):
            commands.add(Command(
                run=[run],
                save=save,
                cwd=cwd,
                bytes_output=bytes_output,
                encoding=encoding,
                stdout=stdout,
                stderr=stderr,
                append=append
            ))
        elif isinstance(run, list):
            for cmd in run:
                if isinstance(cmd, (str, list)):
                    commands.add(Command(
                        run=[cmd] if isinstance(cmd, str) else cmd,
                        save=save,
                        cwd=cwd,
                        bytes_output=bytes_output,
                        encoding=encoding,
                        stdout=stdout,
                        stderr=stderr,
                        append=append
                    ))
                elif isinstance(cmd, dict):
                    self._parse_expanded_commands(cmd, commands)
                else:
                    raise ValueError("Invalid command format in 'run' list.")
        else:
            raise ValueError("'run' must be str or list in expanded syntax.")

    def create_command(self, cmd_input: Mapping) -> Command:
        return Command(
            run=cmd_input.get('run'),
            save=cmd_input.get('save', False),
            cwd=cmd_input.get('cwd'),
            bytes_output=cmd_input.get('bytes', False),
            encoding=cmd_input.get('encoding'),
            stdout=cmd_input.get('stdout'),
            stderr=cmd_input.get('stderr'),
            append=cmd_input.get('append', False)
        )

    async def run_step(self) -> None:
        if not self.commands:
            return

        results = []
        tasks = []

        for cmd in self.commands:
            if isinstance(cmd.run, list):
                for sub_cmd in cmd.run:
                    tasks.append(self._run_command(sub_cmd, cmd))
            else:
                tasks.append(self._run_command(cmd.run, cmd))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        if any(cmd.save for cmd in self.commands):
            self.context['cmdOut'] = results

    async def _run_command(self, cmd: Union[str, List[str]], config: Command) -> Union[SubprocessResult, Exception]:
        try:
            proc = await asyncio.create_subprocess_shell(
                ' '.join(cmd) if isinstance(cmd, list) else cmd,
                stdout=asyncio.subprocess.PIPE if config.save or config.stdout else None,
                stderr=asyncio.subprocess.PIPE if config.save or config.stderr else None,
                cwd=str(config.cwd) if config.cwd else None,
                shell=self.is_shell
            )

            stdout, stderr = await proc.communicate()

            if config.save:
                if config.bytes_output:
                    stdout_result = stdout
                    stderr_result = stderr
                else:
                    encoding = config.encoding or None
                    stdout_result = stdout.decode(
                        encoding).rstrip() if stdout else None
                    stderr_result = stderr.decode(
                        encoding).rstrip() if stderr else None
            else:
                stdout_result = None
                stderr_result = None

            return SubprocessResult(
                cmd=cmd,
                returncode=proc.returncode,
                stdout=stdout_result,
                stderr=stderr_result
            )
        except Exception as e:
            return e
