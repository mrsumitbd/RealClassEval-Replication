
class CommandDispatcher:

    def __init__(self):
        self.commands = {}

    def command(self, fn):
        self.commands[fn.__name__] = fn
        return fn

    def execute_command(self, command, args=None):
        if args is None:
            args = []
        if command in self.commands:
            return self.commands[command](*args)
        else:
            raise ValueError(f"Command '{command}' not found")

    def bound(self, instance):
        bound_commands = CommandDispatcher()
        for name, func in self.commands.items():
            bound_commands.commands[name] = func.__get__(
                instance, instance.__class__)
        return bound_commands
