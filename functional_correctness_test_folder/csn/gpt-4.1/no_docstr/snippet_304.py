
class CommandDispatcher:

    def __init__(self):
        self._commands = {}

    def command(self, fn):
        self._commands[fn.__name__] = fn
        return fn

    def execute_command(self, command, args=None):
        if command not in self._commands:
            raise ValueError(f"Command '{command}' not found")
        fn = self._commands[command]
        if args is None:
            args = []
        return fn(*args)

    def bound(self, instance):
        dispatcher = CommandDispatcher()
        for name, fn in self._commands.items():
            # Bind the function to the instance if it's a method
            bound_fn = fn.__get__(instance, instance.__class__)
            dispatcher._commands[name] = bound_fn
        return dispatcher
