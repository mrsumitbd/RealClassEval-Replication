
class CommandDispatcher:

    def __init__(self):
        self.commands = {}

    def command(self, fn):
        self.commands[fn.__name__] = fn
        return fn

    def execute_command(self, command, args=None):
        if command in self.commands:
            if args is not None:
                return self.commands[command](*args)
            else:
                return self.commands[command]()
        else:
            raise ValueError(f"Command '{command}' not found")

    def bound(self, instance):
        for command_name, command_fn in self.commands.items():
            setattr(instance, command_name, command_fn)
