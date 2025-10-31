
import re


class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        '''Check if a line starts a shell control structure.'''
        # Check for common shell control structure starts like if, for, while, case
        return bool(re.match(r'^\s*(if|for|while|case)\b', line))

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        # Check for common shell control structure ends like fi, done, esac
        return bool(re.match(r'^\s*(fi|done|esac)\b', line))

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        # Check for common shell operators like &&, ||, ;, |, &, (, )
        return bool(re.search(r'\s*(\&\&|\|\||;|\||\(|\))\s*', line))
