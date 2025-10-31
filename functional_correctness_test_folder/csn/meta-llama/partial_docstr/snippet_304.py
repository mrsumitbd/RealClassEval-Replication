
class CommandDispatcher:

    def __init__(self):
        '''
        Create command dictionary
        '''
        self.commands = {}

    def command(self, fn):
        '''
        Add method or function to dispatcher. Can be use as a nice
        decorator.
        :param fn: function or method
        :type fn: function
        :return: the same function
        :rtype: function
        '''
        self.commands[fn.__name__] = fn
        return fn

    def execute_command(self, command, args=None, kwargs=None):
        '''
        Execute a command with given arguments.
        :param command: command to be executed
        :type command: str
        :param args: positional arguments for the command
        :type args: list or tuple
        :param kwargs: keyword arguments for the command
        :type kwargs: dict
        :return: result of the command execution
        '''
        if kwargs is None:
            kwargs = {}
        if args is None:
            args = []
        if command in self.commands:
            return self.commands[command](*args, **kwargs)
        else:
            raise ValueError(f"Unknown command: {command}")

    def bound(self, instance):
        '''
        Bind the dispatcher to an instance. All commands will be executed
        as methods of the instance.
        :param instance: instance to bind to
        :type instance: object
        :return: a new CommandDispatcher instance bound to the given instance
        :rtype: CommandDispatcher
        '''
        bound_dispatcher = CommandDispatcher()
        for command, fn in self.commands.items():
            bound_dispatcher.commands[command] = fn.__get__(instance)
        return bound_dispatcher
