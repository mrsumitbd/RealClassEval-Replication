
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
        i = 0
        while i < len(argument_list):
            arg = argument_list[i]
            if arg in self.options:
                option = self.options[arg]
                if option.get('has_value', False):
                    if i + 1 < len(argument_list):
                        value = argument_list[i + 1]
                        result[option['cleaned_name']] = value
                        i += 2
                    else:
                        result[option['cleaned_name']] = None
                        i += 1
                else:
                    result[option['cleaned_name']] = True
                    i += 1
            elif arg in self.arguments:
                argument = self.arguments[arg]
                result[argument['cleaned_name']] = argument_list[i +
                                                                 1] if i + 1 < len(argument_list) else None
                i += 2
            else:
                i += 1
        return result
