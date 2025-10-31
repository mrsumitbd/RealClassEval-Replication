
class ArgumentProcessor:

    def __init__(self, options, arguments):
        self.options = options
        self.arguments = arguments

    def process(self, argument_list):
        processed = {}
        for arg in argument_list:
            if arg in self.options:
                processed[arg] = True
            elif arg in self.arguments:
                processed[self.arguments[arg]
                          ] = argument_list[argument_list.index(arg) + 1]
        return processed
