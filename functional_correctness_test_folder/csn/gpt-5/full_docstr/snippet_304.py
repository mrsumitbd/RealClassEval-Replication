import inspect


class CommandDispatcher:
    '''
    A simple class for command dictionary. A command is a function
    which can take named parameters.
    '''

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
            raise TypeError("fn must be callable")
        self._commands[fn.__name__] = fn
        return fn

    def execute_command(self, command, args=None):
        '''
        Execute a command
        :param command: name of the command
        :type command: str
        :param args: optional named arguments for command
        :type args: dict
        :return: the result of command
        :raises KeyError: if command is not found
        '''
        if command not in self._commands:
            raise KeyError(f"Command not found: {command}")
        fn = self._commands[command]
        if args is None:
            return fn()
        if not isinstance(args, dict):
            raise TypeError("args must be a dict of keyword arguments")
        return fn(**args)

    def bound(self, instance):
        '''
        Return a new dispatcher, which will switch all command functions
        with bounded methods of given instance matched by name. It will
        match only regular methods.
        :param instance: object instance
        :type instance: object
        :return: new Dispatcher
        :rtype: CommandDispatcher
        '''
        new_dispatcher = CommandDispatcher()
        cls = type(instance)
        for name, func in self._commands.items():
            bound_callable = func
            try:
                raw_attr = inspect.getattr_static(cls, name)
            except AttributeError:
                raw_attr = None

            if raw_attr is not None and inspect.isfunction(raw_attr):
                candidate = getattr(instance, name, None)
                if inspect.ismethod(candidate):
                    bound_callable = candidate

            new_dispatcher._commands[name] = bound_callable
        return new_dispatcher
