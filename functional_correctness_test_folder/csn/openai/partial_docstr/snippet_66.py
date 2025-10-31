
class ArgumentProcessor:
    def __init__(self, options, arguments):
        """
        :param options: list of option strings (e.g. ['-h', '--output'])
        :param arguments: list of positional argument names (e.g. ['input_file'])
        """
        # Map each option to a cleaned name (e.g. '--output' -> 'output')
        self.options_map = {opt: self._clean_name(opt) for opt in options}
        self.positional_names = arguments

    def _clean_name(self, name):
        """Remove leading dashes and replace remaining dashes with underscores."""
        return name.lstrip('-').replace('-', '_')

    def process(self, argument_list):
        """
        :param argument_list: list of str, input from user
        :return: dict: {"cleaned_arg_name": "value"}
        """
        result = {}

        # Initialize defaults for options
        for dest in self.options_map.values():
            result[dest] = None

        pos_index = 0
        i = 0
        while i < len(argument_list):
            token = argument_list[i]
            if token.startswith('-'):  # option
                if token in self.options_map:
                    dest = self.options_map[token]
                    # If next token exists and is not another option, treat it as value
                    if i + 1 < len(argument_list) and not argument_list[i + 1].startswith('-'):
                        result[dest] = argument_list[i + 1]
                        i += 2
                    else:
                        # flag option (boolean)
                        result[dest] = True
                        i += 1
                else:
                    # Unknown option: skip it
                    i += 1
            else:  # positional argument
                if pos_index < len(self.positional_names):
                    dest = self.positional_names[pos_index]
                    result[dest] = token
                    pos_index += 1
                i += 1

        return result
