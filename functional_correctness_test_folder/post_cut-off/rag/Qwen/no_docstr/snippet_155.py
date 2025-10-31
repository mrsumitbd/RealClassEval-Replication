
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
        return '=' in line

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
        if use_spaces:
            return re.sub(r'\s*=\s*', ' = ', line)
        else:
            return re.sub(r'\s*=\s*', '=', line)

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
        if space_before and space_after:
            formatted_line = re.sub(r'\s*:\s*', ' : ', line)
        elif space_before:
            formatted_line = re.sub(r'\s*:\s*', ' :', line)
        elif space_after:
            formatted_line = re.sub(r'\s*:\s*', ': ', line)
        else:
            formatted_line = re.sub(r'\s*:\s*', ':', line)

        return formatted_line if formatted_line != line else None

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
        if space_after_colon:
            formatted_line = re.sub(r'\s*:\s*', ': ', line)
        else:
            formatted_line = re.sub(r'\s*:\s*', ':', line)

        return formatted_line if formatted_line != line else None

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        '''
        Check if line is a conditional directive.
        Args:
            line: The line to check
        Returns:
            True if this is a conditional directive
        '''
        return line.strip().startswith(('if', 'elif', 'else', 'ifdef', 'ifndef', 'endif'))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        '''
        Get the appropriate indentation level for conditional directives.
        Args:
            line: The conditional directive line
        Returns:
            Number of spaces for indentation
        '''
        stripped_line = line.lstrip()
        return len(line) - len(stripped_line)
