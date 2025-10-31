
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
        self._commands[fn.__name__] = fn
        return fn

    def execute_command(self, command, args=None):
        if command not in self._commands:
            raise ValueError(f"Command '{command}' not found")
        fn = self._commands[command]
        if args is None:
            return fn()
        if isinstance(args, dict):
            return fn(**args)
        elif isinstance(args, (list, tuple)):
            return fn(*args)
        else:
            return fn(args)

    def bound(self, instance):
        dispatcher = CommandDispatcher()
        for name, fn in self._commands.items():
            # Bind method if it's a function (not already bound)
            bound_fn = fn
            if hasattr(fn, "__get__"):
                bound_fn = fn.__get__(instance, instance.__class__)
            dispatcher._commands[name] = bound_fn
        return dispatcher
