class CommandDispatcher:

    def __init__(self):
        '''
        Create command dictionary
        '''
        self._commands = {}

    def command(self, fn):
        '''
        Add method or function to dispatcher. Can be use as a nice
        decorator.
        :param fn: function or method
        :type fn: function
        :return: the same function
        :rtype: function
        '''
        if not callable(fn):
            raise TypeError("Command must be callable")
        self._commands[fn.__name__] = fn
        return fn

    def execute_command(self, command, args=None):
        if isinstance(command, str):
            try:
                fn = self._commands[command]
            except KeyError:
                raise KeyError(f"Unknown command: {command}")
        elif callable(command):
            fn = command
        else:
            raise TypeError(
                "command must be a command name (str) or a callable")

        if args is None:
            return fn()
        if isinstance(args, dict):
            return fn(**args)
        if isinstance(args, (list, tuple)):
            return fn(*args)
        return fn(args)

    def bound(self, instance):
        import types
        import inspect

        bound_dispatcher = CommandDispatcher()
        for name, fn in self._commands.items():
            bound_fn = fn
            # If it's already a bound method, keep as is
            if inspect.ismethod(fn) and fn.__self__ is not None:
                bound_fn = fn
            # If it's a plain function, bind it to the instance as a method
            elif inspect.isfunction(fn):
                bound_fn = types.MethodType(fn, instance)
            # Otherwise (callable objects, etc.), leave as is
            bound_dispatcher._commands[name] = bound_fn
        return bound_dispatcher
