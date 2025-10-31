class CommandDispatcher:

    def __init__(self):
        self._commands = {}

    def command(self, fn):
        self._commands[fn.__name__] = fn
        return fn

    def execute_command(self, command, args=None):
        if isinstance(command, str):
            if command not in self._commands:
                raise KeyError(f"Unknown command: {command}")
            fn = self._commands[command]
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
        # Fallback: single positional argument
        return fn(args)

    def bound(self, instance):
        dispatcher = self

        class _BoundDispatcher:
            def __init__(self, disp, inst):
                self._disp = disp
                self._inst = inst

            def execute_command(self, command, args=None):
                if isinstance(command, str):
                    if command not in self._disp._commands:
                        raise KeyError(f"Unknown command: {command}")
                    fn = self._disp._commands[command]
                elif callable(command):
                    fn = command
                else:
                    raise TypeError(
                        "command must be a command name (str) or a callable")

                # Bind function to instance if possible (descriptor protocol)
                if hasattr(fn, "__get__"):
                    bound_fn = fn.__get__(self._inst, type(self._inst))
                else:
                    bound_fn = fn

                if args is None:
                    return bound_fn()
                if isinstance(args, dict):
                    return bound_fn(**args)
                if isinstance(args, (list, tuple)):
                    return bound_fn(*args)
                return bound_fn(args)

            def command(self, fn):
                return self._disp.command(fn)

        return _BoundDispatcher(dispatcher, instance)
