
class ArgumentProcessor:

    def __init__(self, options, arguments):

        self.options = options
        self.arguments = arguments

    def process(self, argument_list):
        '''
        :param argument_list: list of str, input from user
        :return: dict:
            {"cleaned_arg_name": "value"}
        '''
        processed_args = {}
        for arg in argument_list:
            if arg in self.options:
                processed_args[self.options[arg]] = self.arguments[arg]
        return processed_args
