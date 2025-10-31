
import types
from collections.abc import Mapping, Sequence


class CommandDispatcher:
    def __init__(self):
        """
        Create command dictionary
        """
        self.commands = {}

    def command(self, fn):
        """
        Add method or function to dispatcher. Can be used as a decorator.
        :param fn: function or method
        :type fn: function
        :return: the same function
        :rtype: function
        """
        name = getattr(fn, "__name__", None)
        if not name:
            raise ValueError("Command function must have a __name__ attribute")
        self.commands[name] = fn
        return fn

    def execute_command(self, command, args=None):
        """
        Execute a registered command.
        :param command: command name (str) or callable
        :param args: arguments to pass to the command
        :return: result of the command
        """
        if callable(command):
            fn = command
        else:
            fn = self.commands.get(command)
            if fn is None:
                raise KeyError(f"Command '{command}' not found")

        if args is None:
            return fn()
        if isinstance(args, Mapping):
            return fn(**args)
        if isinstance(args, (Sequence, tuple)):
            return fn(*args)
        # single non-iterable argument
        return fn(args)

    def bound(self, instance):
        """
        Return a new dispatcher with all commands bound to the given instance.
        :param instance: object to bind commands to
        :return: CommandDispatcher
        """
        bound_dispatcher = CommandDispatcher()
        for name, fn in self.commands.items():
            # Bind the function to the instance if it is a function
            if isinstance(fn, types.FunctionType):
                bound_dispatcher.commands[name] = types.MethodType(
                    fn, instance)
            else:
                # If it's already a method or callable, keep it as is
                bound_dispatcher.commands[name] = fn
        return bound_dispatcher
