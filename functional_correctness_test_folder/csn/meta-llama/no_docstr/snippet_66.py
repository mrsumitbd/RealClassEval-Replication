
class ArgumentProcessor:

    def __init__(self, options, arguments):
        """
        Initialize the ArgumentProcessor.

        :param options: A list of valid options (e.g., ['-h', '--help'])
        :param arguments: A list of valid arguments (e.g., ['input_file', 'output_file'])
        """
        self.options = options
        self.arguments = arguments

    def process(self, argument_list):
        """
        Process the given argument list.

        :param argument_list: A list of command-line arguments
        :return: A dictionary containing the parsed options and arguments
        """
        parsed_args = {'options': [], 'arguments': {}}

        # Separate options and arguments
        args = []
        for arg in argument_list:
            if arg in self.options:
                parsed_args['options'].append(arg)
            else:
                args.append(arg)

        # Check if the number of provided arguments matches the expected number
        if len(args) != len(self.arguments):
            raise ValueError("Invalid number of arguments. Expected {} but got {}.".format(
                len(self.arguments), len(args)))

        # Map arguments to their corresponding values
        for i, arg in enumerate(self.arguments):
            parsed_args['arguments'][arg] = args[i]

        return parsed_args


# Example usage:
if __name__ == "__main__":
    processor = ArgumentProcessor(
        ['-h', '--help'], ['input_file', 'output_file'])
    argument_list = ['-h', 'data.txt', 'result.txt']
    result = processor.process(argument_list)
    print(result)
