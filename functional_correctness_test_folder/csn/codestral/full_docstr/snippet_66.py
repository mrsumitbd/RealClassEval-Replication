
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
                if i + 1 < len(argument_list) and argument_list[i + 1] not in self.options:
                    result[arg] = argument_list[i + 1]
                    i += 2
                else:
                    result[arg] = True
                    i += 1
            elif arg in self.arguments:
                result[arg] = True
                i += 1
            else:
                i += 1
        return result
