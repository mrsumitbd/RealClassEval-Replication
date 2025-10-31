
class CommandDispatcher:

    def __init__(self):
        self._commands = {}

    def command(self, fn):
        self._commands[fn.__name__] = fn
        return fn

    def execute_command(self, command, args=None):
        if command not in self._commands:
            raise ValueError(f"Command '{command}' not found")
        if args is None:
            return self._commands[command]()
        return self._commands[command](*args)

    def bound(self, instance):
        bound_dispatcher = CommandDispatcher()
        for name, fn in self._commands.items():
            bound_fn = lambda *args, fn=fn, instance=instance: fn(
                instance, *args)
            bound_dispatcher._commands[name] = bound_fn
        return bound_dispatcher
