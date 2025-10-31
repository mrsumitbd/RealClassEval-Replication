
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
            raise KeyError(f"Command '{command}' not found")
        fn = self._commands[command]
        if args is None:
            args = {}
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
        import types
        new_dispatcher = CommandDispatcher()
        for name, fn in self._commands.items():
            # Check if instance has a method with the same name
            bound_method = getattr(instance, name, None)
            if bound_method is not None and isinstance(bound_method, types.MethodType):
                new_dispatcher._commands[name] = bound_method
            else:
                new_dispatcher._commands[name] = fn
        return new_dispatcher
