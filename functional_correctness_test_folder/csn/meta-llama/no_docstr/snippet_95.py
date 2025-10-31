
from typing import Mapping


class Context:
    # Assuming Context is defined elsewhere
    pass


class Command:
    # Assuming Command is defined elsewhere
    pass


class AsyncCmdStep:

    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
        """
        Initialize an AsyncCmdStep instance.

        Args:
        - name (str): The name of the step.
        - context (Context): The context in which the step is executed.
        - is_shell (bool): Whether the command should be executed through a shell. Defaults to False.
        """
        self.name = name
        self.context = context
        self.is_shell = is_shell
        self.command = None

    def create_command(self, cmd_input: Mapping) -> Command:
        """
        Create a Command instance based on the provided input.

        Args:
        - cmd_input (Mapping): A mapping containing the command details.

        Returns:
        - Command: The created Command instance.
        """
        # Assuming Command has a constructor that accepts cmd_input and is_shell
        self.command = Command(cmd_input, self.is_shell)
        return self.command

    async def run_step(self) -> None:
        """
        Run the step asynchronously.

        This method assumes that the command has been created using create_command.
        """
        if self.command is None:
            raise ValueError("Command has not been created")

        # Assuming Command has a method to run asynchronously
        await self.command.run_async()
