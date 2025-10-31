
from typing import Mapping


class Context:
    # Assuming Context class is defined elsewhere
    pass


class Command:
    # Assuming Command class is defined elsewhere
    def __init__(self, *args, **kwargs):
        pass

    def execute(self):
        # Assuming this method is defined in Command class
        pass


class CmdStep:

    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
        self.name = name
        self.context = context
        self.is_shell = is_shell
        self.command = None

    def create_command(self, cmd_input: Mapping) -> Command:
        # Assuming Command class has a constructor that accepts the command and is_shell flag
        self.command = Command(cmd_input, self.is_shell)
        return self.command

    def run_step(self) -> None:
        if self.command is None:
            raise ValueError(
                "Command is not created. Call create_command first.")
        self.command.execute()
