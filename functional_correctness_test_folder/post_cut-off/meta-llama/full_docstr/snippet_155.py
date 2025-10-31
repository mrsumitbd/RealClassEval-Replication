
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
                                '%=', '//=', '**=', '&=', '|=', '^=', '<<=', '>>=']
        for operator in assignment_operators:
            if operator in line:
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
                                '%=', '//=', '**=', '&=', '|=', '^=', '<<=', '>>=']
        for operator in assignment_operators:
            if operator in line:
                if use_spaces:
                    line = line.replace(operator, f' {operator} ')
                else:
                    line = line.replace(f' {operator} ', operator)
                    line = line.replace(f' {operator}', operator)
                    line = line.replace(f'{operator} ', operator)
        return line.strip()

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

        parts = line.split(':')
        if len(parts) > 2:
            return None  # More than one colon, don't format

        before_colon = parts[0].rstrip()
        after_colon = parts[1].lstrip()

        formatted_line = before_colon
        if space_before:
            formatted_line += ' :'
        else:
            formatted_line += ':'

        if space_after:
            formatted_line += ' ' + after_colon
        else:
            formatted_line += after_colon

        if formatted_line == line:
            return None
        return formatted_line

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
        return PatternUtils.format_target_colon(line, space_before=False, space_after=space_after_colon)

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        '''
        Check if line is a conditional directive.
        Args:
            line: The line to check
        Returns:
            True if this is a conditional directive
        '''
        line = line.strip()
        conditional_directives = ['ifeq', 'ifneq',
                                  'ifdef', 'ifndef', 'else', 'endif']
        for directive in conditional_directives:
            if line.startswith(directive):
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
        line = line.strip()
        if line.startswith('ifeq') or line.startswith('ifneq') or line.startswith('ifdef') or line.startswith('ifndef'):
            return 0
        elif line.startswith('else') or line.startswith('endif'):
            return -1  # Decrease indentation level
        else:
            raise ValueError("Not a conditional directive")
