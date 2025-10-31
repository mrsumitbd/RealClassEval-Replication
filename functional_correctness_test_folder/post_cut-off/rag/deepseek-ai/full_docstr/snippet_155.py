
import re
from typing import Optional


class PatternUtils:
    '''Common pattern matching utilities used across formatting rules.'''
    @staticmethod
    def contains_assignment(line: str) -> bool:
        '''
        Check if line contains an assignment operator.
        Args:
            line: The line to check
        Returns:
            True if line contains assignment operators
        '''
        return '=' in line or '+=' in line or ':=' in line or '?=' in line

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        '''
        Apply consistent spacing around assignment operators.
        Args:
            line: The line to format
            use_spaces: Whether to use spaces around operators
        Returns:
            The formatted line
        '''
        if not use_spaces:
            line = re.sub(r'\s*([+:]?=\??)\s*', r'\1', line)
        else:
            line = re.sub(r'\s*([+:]?=\??)\s*', r' \1 ', line)
        return line

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        '''
        Format colon spacing in target definitions.
        Args:
            line: The line to format
            space_before: Whether to add space before colon
            space_after: Whether to add space after colon
        Returns:
            Formatted line or None if no changes needed
        '''
        pattern = r'([^\s:])\s*:\s*([^\s]|$)'
        replacement = r'\1' + (' :' if space_before else ':') + \
            (' ' if space_after else '') + r'\2'
        new_line = re.sub(pattern, replacement, line)
        return new_line if new_line != line else None

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        '''
        Format spacing in pattern rules.
        Args:
            line: The line to format
            space_after_colon: Whether to add space after colon
        Returns:
            Formatted line or None if no changes needed
        '''
        pattern = r'([^%]):([^=]|$)'
        replacement = r'\1:' + (' ' if space_after_colon else '') + r'\2'
        new_line = re.sub(pattern, replacement, line)
        return new_line if new_line != line else None

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        '''
        Check if line is a conditional directive.
        Args:
            line: The line to check
        Returns:
            True if this is a conditional directive
        '''
        return line.strip().startswith(('ifeq', 'ifneq', 'ifdef', 'ifndef'))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        '''
        Get the appropriate indentation level for conditional directives.
        Args:
            line: The conditional directive line
        Returns:
            Number of spaces for indentation
        '''
        return 4 if line.strip().startswith(('ifeq', 'ifneq', 'ifdef', 'ifndef')) else 0
