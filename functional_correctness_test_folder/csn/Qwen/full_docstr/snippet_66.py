
class ArgumentProcessor:
    '''
    responsible for parsing given list of arguments
    '''

    def __init__(self, options, arguments):
        '''
        :param options: list of options
        :param arguments: list of arguments
        '''
        self.options = options
        self.arguments = arguments

    def process(self, argument_list):
        '''
        :param argument_list: list of str, input from user
        :return: dict:
            {"cleaned_arg_name": "value"}
        '''
        result = {}
        it = iter(argument_list)
        for arg in it:
            if arg in self.options:
                try:
                    value = next(it)
                    if not value.startswith('-'):
                        result[arg.lstrip('-')] = value
                except StopIteration:
                    pass
            else:
                for option in self.options:
                    if arg.startswith(option + '='):
                        result[option.lstrip('-')] = arg.split('=', 1)[1]
        return result
