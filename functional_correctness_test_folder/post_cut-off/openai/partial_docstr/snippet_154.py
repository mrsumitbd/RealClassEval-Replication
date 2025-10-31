
import re
from typing import Pattern


class ShellUtils:
    '''Utilities for processing shell commands within Makefile recipes.'''

    # Regular expressions for detecting shell control structures
    _control_start_re: Pattern = re.compile(
        r'^\s*(if|for|while|case|function|select|until|do|elif|else|then)\b',
        re.IGNORECASE
    )
    _control_end_re: Pattern = re.compile(
        r'^\s*(fi|done|esac|})\b',
        re.IGNORECASE
    )

    # Regular expression for detecting shell operators that imply structure
    _operator_re: Pattern = re.compile(
        r'(?<![^\s])(?:&&|\|\||\||;|&|>>|>|<<|<|[|&])(?!=)',
        re.IGNORECASE
    )

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        """
        Return True if the line starts a shell control structure.
        """
        return bool(ShellUtils._control_start_re.match(line))

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        """
        Check if a line ends a shell control structure.
        """
        return bool(ShellUtils._control_end_re.match(line))

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        """
        Check if content contains shell operators that suggest deliberate structure.
        """
        return bool(ShellUtils._operator_re.search(line))
