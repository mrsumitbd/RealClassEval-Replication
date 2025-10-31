
class ArgumentProcessor:
    '''
    responsible for parsing given list of arguments
    '''

    def __init__(self, options, arguments):
        '''
        :param options: list of options
        :param arguments: list of arguments
        '''
        self.options = set(options)
        self.arguments = set(arguments)

    def process(self, argument_list):
        '''
        :param argument_list: list of str, input from user
        :return: dict:
            {"cleaned_arg_name": "value"}
        '''
        result = {}
        i = 0
        n = len(argument_list)
        while i < n:
            arg = argument_list[i]
            if arg.startswith('--'):
                name = arg[2:]
                if name in self.options:
                    # Option, check if next is value
                    if i + 1 < n and not argument_list[i + 1].startswith('-'):
                        result[name] = argument_list[i + 1]
                        i += 2
                    else:
                        result[name] = True
                        i += 1
                elif name in self.arguments:
                    # Argument, must have value
                    if i + 1 < n and not argument_list[i + 1].startswith('-'):
                        result[name] = argument_list[i + 1]
                        i += 2
                    else:
                        result[name] = None
                        i += 1
                else:
                    i += 1
            elif arg.startswith('-') and len(arg) > 1:
                name = arg[1:]
                if name in self.options:
                    if i + 1 < n and not argument_list[i + 1].startswith('-'):
                        result[name] = argument_list[i + 1]
                        i += 2
                    else:
                        result[name] = True
                        i += 1
                elif name in self.arguments:
                    if i + 1 < n and not argument_list[i + 1].startswith('-'):
                        result[name] = argument_list[i + 1]
                        i += 2
                    else:
                        result[name] = None
                        i += 1
                else:
                    i += 1
            else:
                i += 1
        return result
