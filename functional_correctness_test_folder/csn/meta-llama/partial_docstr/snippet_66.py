
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
        result = {}
        arg_index = 0
        while arg_index < len(argument_list):
            arg = argument_list[arg_index]
            if arg.startswith('-'):
                arg_name = arg.lstrip('-')
                if arg_name in self.options:
                    if arg_index + 1 < len(argument_list) and not argument_list[arg_index + 1].startswith('-'):
                        result[arg_name] = argument_list[arg_index + 1]
                        arg_index += 2
                    else:
                        result[arg_name] = True
                        arg_index += 1
                else:
                    raise ValueError(f"Unknown option: {arg}")
            else:
                if self.arguments:
                    arg_name = self.arguments.pop(0)
                    result[arg_name] = arg
                    arg_index += 1
                else:
                    raise ValueError(f"Unexpected argument: {arg}")
        return result
