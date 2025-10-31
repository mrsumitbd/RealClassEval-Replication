
class ArgumentProcessor:

    def __init__(self, options, arguments):
        self.options = options
        self.arguments = arguments

    def process(self, argument_list):
        processed_arguments = []
        for arg in argument_list:
            if arg in self.options:
                processed_arguments.append((arg, self.options[arg]))
            elif arg in self.arguments:
                processed_arguments.append((arg, self.arguments[arg]))
            else:
                processed_arguments.append((arg, None))
        return processed_arguments
