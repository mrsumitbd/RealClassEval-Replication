
from typing import Mapping
# Assuming these are defined in some_module
from some_module import Context, Command


class CmdStep:

    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
        self.name = name
        self.context = context
        self.is_shell = is_shell

    def create_command(self, cmd_input: Mapping) -> Command:
        # Assuming Command can be initialized with a command string and is_shell flag
        command_string = self._generate_command_string(cmd_input)
        return Command(command_string, is_shell=self.is_shell)

    def run_step(self) -> None:
        command = self.create_command(self.context.get_input())
        command.execute()

    def _generate_command_string(self, cmd_input: Mapping) -> str:
        # This method should be implemented based on how the command string is constructed
        # For demonstration, let's assume cmd_input is a dictionary with keys as command parts
        return ' '.join(cmd_input.values())
