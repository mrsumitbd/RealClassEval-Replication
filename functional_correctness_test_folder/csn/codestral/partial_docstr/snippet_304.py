
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

    def execute_command(self, command, args=None):
        if command in self.commands:
            if args is not None:
                return self.commands[command](*args)
            else:
                return self.commands[command]()
        else:
            raise ValueError(f"Command '{command}' not found")

    def bound(self, instance):
        for command_name, command in self.commands.items():
            if callable(command):
                self.commands[command_name] = command.__get__(
                    instance, instance.__class__)
