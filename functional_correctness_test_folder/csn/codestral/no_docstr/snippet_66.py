
class ArgumentProcessor:

    def __init__(self, options, arguments):

        self.options = options
        self.arguments = arguments

    def process(self, argument_list):

        processed_args = {}
        for arg in argument_list:
            if arg in self.options:
                processed_args[arg] = self.options[arg]
            elif arg in self.arguments:
                processed_args[arg] = self.arguments[arg]
        return processed_args
