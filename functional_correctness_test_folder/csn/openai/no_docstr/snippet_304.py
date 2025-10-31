
import types
from collections.abc import Mapping, Sequence


class CommandDispatcher:
    def __init__(self):
        # Mapping of command name to callable
        self.commands = {}

    def command(self, fn):
        """
        Decorator to register a function as a command.
        The command name defaults to the function's __name__.
        """
        name = fn.__name__
        self.commands[name] = fn
        return fn

    def execute_command(self, command, args=None):
        """
        Execute a registered command by name or callable.
        `args` can be:
            - None: call with no arguments
            - Sequence (list/tuple): passed as positional arguments
            - Mapping (dict): passed as keyword arguments
        """
        # Resolve command to callable
        if isinstance(command, str):
            fn = self.commands.get(command)
            if fn is None:
                raise KeyError(f"Command '{command}' not found")
        elif callable(command):
            fn = command
        else:
            raise TypeError("command must be a string or callable")

        # Call with appropriate arguments
        if args is None:
            return fn()
        if isinstance(args, Mapping):
            return fn(**args)
        if isinstance(args, Sequence) and not isinstance(args, (str, bytes)):
            return fn(*args)
        # Fallback: treat as single positional argument
        return fn(args)

    def bound(self, instance):
        """
        Return a new CommandDispatcher where each command is bound to the given instance.
        Useful for dispatching instance methods.
        """
        bound_dispatcher = CommandDispatcher()
        for name, fn in self.commands.items():
            # Bind the function to the instance
            bound_fn = types.MethodType(fn, instance)
            bound_dispatcher.commands[name] = bound_fn
        return bound_dispatcher
