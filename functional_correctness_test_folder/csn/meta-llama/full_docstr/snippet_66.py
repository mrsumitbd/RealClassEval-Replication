
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
        i = 0
        while i < len(argument_list):
            arg = argument_list[i]
            if arg in self.options:
                result[arg.lstrip('-')] = True
                i += 1
            elif arg in self.arguments:
                if i + 1 < len(argument_list) and argument_list[i + 1] not in self.options and argument_list[i + 1] not in self.arguments:
                    result[arg.lstrip('-')] = argument_list[i + 1]
                    i += 2
                else:
                    raise ValueError(f"Missing value for argument {arg}")
            else:
                raise ValueError(f"Unknown argument or option: {arg}")
        return result
