
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
        '''
        Execute the command with the given args.
        :param command: command name
        :type command: str
        :param args: arguments for the command
        :type args: dict or None
        :return: result of the command execution
        :rtype: any
        '''
        if command not in self._commands:
            raise ValueError(f"Command '{command}' not found")
        if args is None:
            args = {}
        return self._commands[command](**args)

    def bound(self, instance):
        '''
        Bind the instance to the commands.
        :param instance: instance to bind
        :type instance: object
        :return: new CommandDispatcher with bound methods
        :rtype: CommandDispatcher
        '''
        bound_dispatcher = CommandDispatcher()
        for name, fn in self._commands.items():
            bound_method = fn.__get__(instance, instance.__class__)
            bound_dispatcher.command(bound_method)
        return bound_dispatcher
