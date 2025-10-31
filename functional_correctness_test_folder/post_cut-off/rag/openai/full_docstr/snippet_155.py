
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
        # Match a single '=' that is not part of '==', '!=', '<=', '>='
        return bool(re.search(r'(?<![=!<>])=(?![=])', line))

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
        # Replace single '=' with spaced or unspaced version
        def repl(match):
            return f' = ' if use_spaces else '='

        return re.sub(r'(?<![=!<>])=(?![=])', repl, line)

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
        # Find a colon that is not part of '::'
        m = re.search(r'(?<!:)(:)(?!:)', line)
        if not m:
            return None

        before = line[:m.start()]
        after = line[m.end():]

        # Determine current spacing
        before_space = before.endswith(' ')
        after_space = after.startswith(' ')

        new_before = before.rstrip()
        new_after = after.lstrip()

        if space_before:
            new_before += ' '
        if space_after:
            new_after = ' ' + new_after

        new_line = new_before + ':' + new_after
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
        # Find colon not part of '::'
        m = re.search(r'(?<!:)(:)(?!:)', line)
        if not m:
            return None

        before = line[:m.start()]
        after = line[m.end():]

        # Strip existing spaces around colon
        before = before.rstrip()
        after = after.lstrip()

        new_line = before + ':' + (' ' if space_after_colon else '') + after
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
        return len(line) - len(line.lstrip(' '))
