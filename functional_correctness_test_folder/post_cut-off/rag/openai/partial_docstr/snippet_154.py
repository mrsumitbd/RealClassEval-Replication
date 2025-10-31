
import re
from typing import Pattern


class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''

    # Regular expressions for detecting shell control structures
    _control_start_re: Pattern[str] = re.compile(
        r'^\s*(if|for|while|case|until|do)\b')
    _control_end_re: Pattern[str] = re.compile(r'^\s*(fi|done|esac)\b')

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        '''Check if a line starts a shell control structure.'''
        return bool(ShellUtils._control_start_re.match(line))

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        '''Check if a line ends a shell control structure.'''
        return bool(ShellUtils._control_end_re.match(line))

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        '''Check if content contains shell operators that suggest deliberate structure.'''
        # Common shell operators that indicate intentional command chaining or grouping
        operators = [
            r'\&\&', r'\|\|', r';', r'\|', r'\&', r'>', r'<', r'>>', r'<<',
            r'\(', r'\)', r'\{', r'\}'
        ]
        pattern = re.compile('|'.join(operators))
        return bool(pattern.search(line))
