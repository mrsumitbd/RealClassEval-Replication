
from typing import Mapping


class CmdStep:

    def __init__(self, name: str, context: 'Context', is_shell: bool = False) -> None:
        self.name = name
        self.context = context
        self.is_shell = is_shell
        self.command = None

    def create_command(self, cmd_input: Mapping) -> 'Command':
        # Assume Command takes (cmd_input, context, is_shell)
        self.command = Command(cmd_input, self.context, self.is_shell)
        return self.command

    def run_step(self) -> None:
        if self.command is None:
            raise RuntimeError(
                "Command not created. Call create_command first.")
        self.command.execute()
