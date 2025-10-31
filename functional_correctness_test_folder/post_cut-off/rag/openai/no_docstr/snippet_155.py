
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
        # Match a single '=' that is not part of '==', '!=', '=>', or '<='
        return bool(re.search(r'(?<![=!<>])=(?!=)', line))

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
        if not PatternUtils.contains_assignment(line):
            return line

        def repl(match):
            left, right = match.group(1), match.group(2)
            if use_spaces:
                return f'{left} = {right}'
            return f'{left}={right}'

        # Replace all assignments in the line
        return re.sub(r'(\S+)\s*=\s*(\S+)', repl, line)

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False,
                            space_after: bool = True) -> Optional[str]:
        '''
        Format colon spacing in target definitions.
        Args:
            line: The line to format
            space_before: Whether to add space before colon
            space_after: Whether to add space after colon
        Returns:
            Formatted line or None if no changes needed
        '''
        # Target definitions are lines that end with a colon and have no trailing content
        m = re.match(r'^(\S+)\s*:\s*(.*)$', line)
        if not m:
            return None

        target, rest = m.group(1), m.group(2)
        # Only format if there is no content after the colon
        if rest.strip():
            return None

        new_colon = ':'  # base colon
        if space_before:
            new_colon = f' {new_colon}'
        if space_after:
            new_colon = f'{new_colon} '

        new_line = f'{target}{new_colon}'.rstrip()
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
        m = re.match(r'^(\S+)\s*:\s*(.*)$', line)
        if not m:
            return None

        key, value = m.group(1), m.group(2)
        new_colon = ':' if not space_after_colon else ': '
        new_line = f'{key}{new_colon}{value}'
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
        return bool(re.match(r'^\s*#?(if|else|elif|endif)\b', line))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        '''
        Get the appropriate indentation level for conditional directives.
        Args:
            line: The conditional directive line
        Returns:
            Number of spaces for indentation
        '''
        # Return the count of leading spaces
        return len(line) - len(line.lstrip(' '))
