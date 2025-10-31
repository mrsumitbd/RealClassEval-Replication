
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
        assignment_operators = ['=', '+=', '-=', '*=', '/=',
                                '%=', '//=', '**=', '>>=', '<<=', '&=', '^=', '|=']
        for op in assignment_operators:
            if op in line:
                return True
        return False

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
        assignment_operators = ['=', '+=', '-=', '*=', '/=',
                                '%=', '//=', '**=', '>>=', '<<=', '&=', '^=', '|=']
        for op in assignment_operators:
            if op in line:
                if use_spaces:
                    line = line.replace(op, f' {op} ')
                else:
                    line = line.replace(op, op)
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
        if ':' not in line:
            return None

        original_line = line
        line = line.replace(' :', ':') if not space_before else line
        line = line.replace(': ', ':') if not space_after else line

        if space_before:
            line = line.replace(':', ' :')
        if space_after:
            line = line.replace(':', ': ')

        return line if line != original_line else None

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
        if ':' not in line:
            return None

        original_line = line
        line = line.replace(': ', ':') if not space_after_colon else line

        if space_after_colon:
            line = line.replace(':', ': ')

        return line if line != original_line else None

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        '''
        Check if line is a conditional directive.
        Args:
            line: The line to check
        Returns:
            True if this is a conditional directive
        '''
        conditional_directives = ['#if', '#elif', '#else', '#endif']
        for directive in conditional_directives:
            if line.strip().startswith(directive):
                return True
        return False

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        '''
        Get the appropriate indentation level for conditional directives.
        Args:
            line: The conditional directive line
        Returns:
            Number of spaces for indentation
        '''
        if not PatternUtils.is_conditional_directive(line):
            return 0

        indent_level = 0
        for directive in ['#if', '#elif', '#else', '#endif']:
            if line.strip().startswith(directive):
                indent_level = line.find(directive)
                break

        return indent_level
