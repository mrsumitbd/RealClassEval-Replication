
class ArgumentProcessor:

    def __init__(self, options, arguments):
        # options: dict of option name to default value
        # arguments: list of positional argument names
        self.options = options.copy() if options else {}
        self.arguments = arguments[:]
        self.reset()

    def reset(self):
        self.parsed_options = self.options.copy()
        self.parsed_arguments = []
        self.extra = []

    def process(self, argument_list):
        self.reset()
        args_iter = iter(argument_list)
        while True:
            try:
                arg = next(args_iter)
            except StopIteration:
                break
            if arg.startswith('--'):
                if '=' in arg:
                    opt, val = arg[2:].split('=', 1)
                    self.parsed_options[opt] = val
                else:
                    opt = arg[2:]
                    # Check if next is a value or another option
                    try:
                        peek = next(args_iter)
                        if peek.startswith('--'):
                            # Boolean flag
                            self.parsed_options[opt] = True
                            # Put back peek
                            args_iter = self._prepend(peek, args_iter)
                        else:
                            self.parsed_options[opt] = peek
                    except StopIteration:
                        self.parsed_options[opt] = True
            else:
                if len(self.parsed_arguments) < len(self.arguments):
                    self.parsed_arguments.append(arg)
                else:
                    self.extra.append(arg)
        # Fill missing positional arguments with None
        while len(self.parsed_arguments) < len(self.arguments):
            self.parsed_arguments.append(None)
        return {
            'options': self.parsed_options,
            'arguments': dict(zip(self.arguments, self.parsed_arguments)),
            'extra': self.extra
        }

    def _prepend(self, value, iterator):
        # Helper to put a value back in front of an iterator
        yield value
        yield from iterator
