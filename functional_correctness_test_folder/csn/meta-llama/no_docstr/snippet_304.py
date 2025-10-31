
class CommandDispatcher:

    def __init__(self):
        self.commands = {}

    def command(self, fn):
        self.commands[fn.__name__] = fn
        return fn

    def execute_command(self, command, args=None):
        if command not in self.commands:
            raise ValueError(f"Unknown command: {command}")

        if args is None:
            args = ()

        return self.commands[command](*args)

    def bound(self, instance):
        bound_dispatcher = CommandDispatcher()
        bound_dispatcher.commands = {name: fn.__get__(
            instance) for name, fn in self.commands.items()}
        return bound_dispatcher
