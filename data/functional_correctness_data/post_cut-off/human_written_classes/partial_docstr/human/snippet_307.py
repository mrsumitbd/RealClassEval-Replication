from tools.terminal import term_support_color
from sys import stderr, stdout
from typing import Dict, List, Optional, TextIO, Tuple

class ArgParse:

    def __init__(self, args: List[str]) -> None:
        self.__bin: str = ''
        self.__args: Dict[str, List[str | Dict[str, str]]] = {'long': [], 'short': []}
        previous_arg_type: str = ''
        for i, arg in enumerate(args):
            if i == 0:
                self.__bin = arg
            elif arg.startswith('--'):
                self.__args['long'].append(arg[2:])
                previous_arg_type = 'long'
            elif arg.startswith('-'):
                self.__args['short'].append(arg[1:])
                previous_arg_type = 'short'
            elif previous_arg_type == 'short':
                self.__args['short'].append({'option': arg})
            elif previous_arg_type == 'long':
                self.__args['long'].append({'option': arg})

    def find_arg(self, __arg: Tuple[str, str]) -> bool:
        """tries to find 'arg' inside the argument list

        Args:
            arg (Tuple[str, str]): a tuple containing a short form of the arg, and long form

        Returns:
            bool: true if one of the arg is found, or false
        """
        for arg in self.__args['short']:
            if not isinstance(arg, Dict) and __arg[0][1:] in arg:
                return True
        for arg in self.__args['long']:
            if not isinstance(arg, Dict) and __arg[1][2:] == arg:
                return True
        return False

    def option_arg(self, __arg: Tuple[str, str]) -> Optional[str]:
        """tries to find and return an option from a given argument

        Args:
            arg (Tuple[str, str]): a tuple containing a short form of the arg, and long form

        Returns:
            Optional[str]: the option given or None
        """
        for i, arg in enumerate(self.__args['short']):
            if isinstance(arg, Dict):
                continue
            if '=' in arg:
                eq_index: int = arg.index('=')
                split_arg: Tuple[str, str] = (arg[:eq_index], arg[eq_index + 1:])
                if len(split_arg[0]) > 1 and split_arg[0][-1] == __arg[0][1:] or (len(split_arg[0]) == 1 and split_arg[0][0] == __arg[0][1:]):
                    return split_arg[1]
            if len(arg) > 1 and arg[0] == __arg[0][1:]:
                return arg[1:]
            if len(arg) > 1:
                for _, c in enumerate(arg):
                    if c == __arg[0][1:] and i + 1 < len(self.__args['short']):
                        next_arg = self.__args['short'][i + 1]
                        if isinstance(next_arg, Dict):
                            return next_arg['option']
            if arg == __arg[0][1:] and i + 1 < len(self.__args['short']):
                next_arg = self.__args['short'][i + 1]
                if isinstance(next_arg, Dict):
                    return next_arg['option']
        for i, arg in enumerate(self.__args['long']):
            if isinstance(arg, Dict):
                continue
            if '=' in arg:
                eq_index: int = arg.index('=')
                split_arg: Tuple[str, str] = (arg[:eq_index], arg[eq_index + 1:])
                if split_arg[0] == __arg[1][2:]:
                    return split_arg[1]
            if arg == __arg[1][2:] and i + 1 < len(self.__args['long']):
                next_arg = self.__args['long'][i + 1]
                if isinstance(next_arg, Dict):
                    return next_arg['option']
        return None

    def arg_print(self, msg: str) -> None:
        sprint(self.__help_stream, msg)

    def print_help_msg(self, stream: Optional[TextIO]):
        self.__help_stream = stream
        use_colors = term_support_color()
        if use_colors:
            RESET = '\x1b[0m'
            BOLD = '\x1b[1m'
            UNDERLINE = '\x1b[4m'
            CYAN = '\x1b[36m'
            GREEN = '\x1b[32m'
            YELLOW = '\x1b[33m'
            BLUE = '\x1b[34m'
            MAGENTA = '\x1b[35m'
            GRAY = '\x1b[90m'
            WHITE = '\x1b[97m'
        else:
            RESET = BOLD = UNDERLINE = CYAN = GREEN = YELLOW = BLUE = MAGENTA = GRAY = WHITE = ''
        self.arg_print(f'\n{BOLD}{CYAN}╭────────────────────────────────────────────────────────────────╮{RESET}')
        self.arg_print(f'{BOLD}{CYAN}│                         BETTER CONTROL                         │{RESET}')
        self.arg_print(f'{BOLD}{CYAN}╰────────────────────────────────────────────────────────────────╯{RESET}\n')
        self.arg_print(f'{BOLD}USAGE:{RESET}')
        self.arg_print(f'  {WHITE}better-control {GRAY}[options]{RESET} \n  {WHITE}control {GRAY}[options]\n')
        self.arg_print(f'{BOLD}OPTIONS:{RESET}')
        self.arg_print(f'{BOLD}{UNDERLINE}General:{RESET}')
        self.arg_print(f'  {GREEN}-h, --help{RESET}                      Prints this help message')
        self.arg_print(f'  {GREEN}-f, --force{RESET}                     Makes the app force to have all dependencies installed')
        self.arg_print(f'  {GREEN}-s, --size{RESET} {YELLOW}<intxint>{RESET}            Sets a custom window size')
        self.arg_print(f'  {GREEN}-L, --lang{RESET}                      Sets the language of the app (en,es,pt)')
        self.arg_print(f'  {GREEN}-m, --minimal{RESET}                   Hides the notebook tabs and only shows the selected tab content\n')
        self.arg_print(f'{BOLD}{UNDERLINE}Tab Selection:{RESET}')
        self.arg_print(f'  {BLUE}-a, --autostart{RESET}                 Starts with the autostart tab open')
        self.arg_print(f'  {BLUE}-B, --battery{RESET}                   Starts with the battery tab open')
        self.arg_print(f'  {BLUE}-b, --bluetooth{RESET}                 Starts with the bluetooth tab open')
        self.arg_print(f'  {BLUE}-d, --display{RESET}                   Starts with the display tab open')
        self.arg_print(f'  {BLUE}-p, --power{RESET}                     Starts with the power tab open')
        self.arg_print(f'  {BLUE}-u, --usbguard{RESET}                  Starts with the usbguard tab open')
        self.arg_print(f'  {BLUE}-V, --volume{RESET}                    Starts with the volume tab open')
        self.arg_print(f'  {BLUE}-v{RESET}                              Also starts with the volume tab open')
        self.arg_print(f'  {BLUE}-w, --wifi{RESET}                      Starts with the wifi tab open\n')
        self.arg_print(f'{BOLD}{UNDERLINE}Logging:{RESET}')
        self.arg_print(f'  {MAGENTA}-l, --log{RESET} {YELLOW}<lvl/file>{RESET}            The program will either log to a file if given a file path,')
        self.arg_print('                                  or output to stdout based on the log level if given')
        self.arg_print('                                  a value between 0 and 3.')
        self.arg_print(f'  {MAGENTA}-r, --redact{RESET}                    Redact sensitive information from logs\n')
        self.arg_print(f'{BOLD}{CYAN}╭────────────────────────────────────────────────────────────────╮{RESET}')
        self.arg_print(f'{BOLD}{CYAN}│         https://github.com/quantumvoid0/better-control         │{RESET}')
        self.arg_print(f'{BOLD}{CYAN}╰────────────────────────────────────────────────────────────────╯{RESET}\n')
        if stream == stderr:
            exit(1)
        else:
            exit(0)