
import re
from collections import OrderedDict


class ArgumentProcessor:
    '''
    responsible for parsing given list of arguments
    '''

    def __init__(self, options, arguments):
        '''
        :param options: list of option strings (e.g. ['--name', '-n'])
        :param arguments: list of positional argument names (e.g. ['file', 'mode'])
        '''
        # Normalize options: map each option to its cleaned name
        self._option_map = {}
        for opt in options:
            cleaned = self._clean_name(opt)
            self._option_map[opt] = cleaned
            # also map short form without leading dash if present
            if opt.startswith('--'):
                short = opt[2:]
                if short:
                    self._option_map['-' + short] = cleaned
            elif opt.startswith('-'):
                long_opt = opt[1:]
                if long_opt:
                    self._option_map['--' + long_opt] = cleaned

        self._positional_names = list(arguments)

    def process(self, argument_list):
        '''
        :param argument_list: list of str, input from user
        :return: dict:
            {"cleaned_arg_name": "value"}
        '''
        result = OrderedDict()
        pos_index = 0
        i = 0
        while i < len(argument_list):
            token = argument_list[i]
            if token.startswith('-'):
                # option
                if '=' in token:
                    opt, val = token.split('=', 1)
                    cleaned = self._option_map.get(opt, self._clean_name(opt))
                    result[cleaned] = val
                else:
                    opt = token
                    cleaned = self._option_map.get(opt, self._clean_name(opt))
                    # look ahead for value if next token is not an option
                    if i + 1 < len(argument_list) and not argument_list[i + 1].startswith('-'):
                        val = argument_list[i + 1]
                        i += 1
                    else:
                        val = True  # flag option
                    result[cleaned] = val
            else:
                # positional argument
                if pos_index < len(self._positional_names):
                    name = self._positional_names[pos_index]
                    result[name] = token
                    pos_index += 1
                else:
                    # ignore extra positional arguments
                    pass
            i += 1
        return result

    @staticmethod
    def _clean_name(name):
        """Remove leading dashes and convert to snake_case."""
        name = re.sub(r'^-+', '', name)
        # replace hyphens with underscores
        name = name.replace('-', '_')
        return name
