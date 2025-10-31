
class CmdStep:

    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
        self.name = name
        self.context = context
        self.is_shell = is_shell

    def create_command(self, cmd_input: Mapping) -> Command:
        command = Command(cmd_input, self.context, self.is_shell)
        return command

    def run_step(self) -> None:
        cmd_input = self.context.get_command_input(self.name)
        command = self.create_command(cmd_input)
        command.execute()
