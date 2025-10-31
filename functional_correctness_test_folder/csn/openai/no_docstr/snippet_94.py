
from typing import Mapping


class CmdStep:
    def __init__(self, name: str, context: 'Context', is_shell: bool = False) -> None:
        self.name = name
        self.context = context
        self.is_shell = is_shell

    def create_command(self, cmd_input: Mapping) -> 'Command':
        # Assume Command can be instantiated with keyword arguments from the mapping
        return Command(**cmd_input)

    def run_step(self) -> None:
        # Retrieve command input from the context if available
        cmd_input = getattr(self.context, "cmd_input", {})
        command = self.create_command(cmd_input)

        # Try to run the command using the context's run/execute method
        if hasattr(self.context, "run"):
            self.context.run(command)
        elif hasattr(self.context, "execute"):
            self.context.execute(command)
        else:
            # Fallback: try to run the command directly
            if hasattr(command, "run"):
                command.run()
            else:
                raise RuntimeError("No method available to run the command")
