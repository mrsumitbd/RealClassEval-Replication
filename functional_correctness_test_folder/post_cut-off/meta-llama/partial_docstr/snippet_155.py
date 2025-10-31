
from typing import Optional


class PatternUtils:

    @staticmethod
    def contains_assignment(line: str) -> bool:
        """Check if a line contains an assignment."""
        return '=' in line and not line.lstrip().startswith('#')

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        """Apply spacing around the assignment operator."""
        parts = line.split('=')
        if len(parts) < 2:
            return line

        operator = ' = ' if use_spaces else '='
        return operator.join([part.rstrip() if i == 0 else part.lstrip() for i, part in enumerate(parts)])

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
        original_line = line

        before_colon = ' ' if space_before else ''
        after_colon = ' ' if space_after else ''

        line = before_colon.join(
            [parts[0].rstrip(), after_colon.join(parts[1:])])

        if line == original_line:
            return None

        return line

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        """Format pattern rule by adjusting spacing after colon."""
        if ':' not in line:
            return None

        parts = line.split(':')
        original_line = line

        after_colon = ' ' if space_after_colon else ''

        line = parts[0].rstrip() + ':' + after_colon + \
            after_colon.join([part.lstrip() for part in parts[1:]])

        if line == original_line:
            return None

        return line

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        """Check if a line is a conditional directive."""
        line = line.lstrip()
        return line.startswith(('ifeq', 'ifneq', 'ifdef', 'ifndef', 'else', 'endif'))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        '''
        Get the appropriate indentation level for conditional directives.
        Args:
            line: The conditional directive line
        Returns:
            Number of spaces for indentation
        '''
        line = line.lstrip()
        if line.startswith(('else', 'endif')):
            return 0
        elif line.startswith(('ifeq', 'ifneq', 'ifdef', 'ifndef')):
            return 0  # Typically, these are not indented
        else:
            return 0  # Default to no indentation for unknown directives
