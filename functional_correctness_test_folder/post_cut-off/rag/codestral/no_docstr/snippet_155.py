
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
        assignment_patterns = [r'=', r'\+=', r'-=', r'\*=', r'/=',
                               r'%=', r'\^=', r'&=', r'\|=', r'>>=', r'<<=', r':=']
        for pattern in assignment_patterns:
            if re.search(pattern, line):
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
        assignment_patterns = [r'=', r'\+=', r'-=', r'\*=', r'/=',
                               r'%=', r'\^=', r'&=', r'\|=', r'>>=', r'<<=', r':=']
        for pattern in assignment_patterns:
            if use_spaces:
                line = re.sub(r'(\s*)(' + pattern + ')(\s*)', r' \2 ', line)
            else:
                line = re.sub(r'(\s*)(' + pattern + ')(\s*)', r'\2', line)
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
        if space_before and space_after:
            line = re.sub(r'(\S):(\S)', r'\1 : \2', line)
        elif space_before:
            line = re.sub(r'(\S):(\S)', r'\1 :\2', line)
        elif space_after:
            line = re.sub(r'(\S):(\S)', r'\1:\2 ', line)
        else:
            line = re.sub(r'(\S):(\S)', r'\1:\2', line)

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
        if space_after_colon:
            line = re.sub(r'(\S):(\S)', r'\1: \2', line)
        else:
            line = re.sub(r'(\S):(\S)', r'\1:\2', line)

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
        conditional_patterns = [r'#if', r'#else', r'#elif', r'#endif']
        for pattern in conditional_patterns:
            if re.search(pattern, line.strip()):
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

        indent = 0
        if '#if' in line:
            indent = 0
        elif '#elif' in line or '#else' in line:
            indent = 4
        elif '#endif' in line:
            indent = 0

        return indent
