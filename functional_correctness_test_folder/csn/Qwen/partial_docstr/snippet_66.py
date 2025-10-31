
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
        arg_iter = iter(argument_list)
        for arg in arg_iter:
            if arg in self.options:
                try:
                    value = next(arg_iter)
                    if value.startswith('-'):
                        raise ValueError(
                            f"Expected value for {arg}, got another option {value}")
                    result[arg] = value
                except StopIteration:
                    raise ValueError(
                        f"Expected value for {arg}, but none provided")
            elif arg in self.arguments:
                result[arg] = True
            else:
                raise ValueError(f"Unknown argument {arg}")
        return result
