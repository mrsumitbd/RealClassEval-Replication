
import re
from typing import Pattern


class ShellUtils:
    """Utilities for processing shell commands within Makefile recipes."""

    # Regular expressions for detecting shell control structures
    _START_RE: Pattern[str] = re.compile(r'^\s*(if|for|while|case|until)\b')
    _END_RE: Pattern[str] = re.compile(r'^\s*(fi|done|esac)\b')
    _OP_RE: Pattern[str] = re.compile(r'(&&|\|\||;|\||\(|\)|\{|\})')

    @staticmethod
    def is_shell_control_start(line: str) -> bool:
        """Check if a line starts a shell control structure."""
        return bool(ShellUtils._START_RE.match(line))

    @staticmethod
    def is_shell_control_end(line: str) -> bool:
        """Check if a line ends a shell control structure."""
        return bool(ShellUtils._END_RE.match(line))

    @staticmethod
    def contains_shell_operators(line: str) -> bool:
        """Check if content contains shell operators that suggest deliberate structure."""
        return bool(ShellUtils._OP_RE.search(line))
