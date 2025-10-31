
from typing import Optional


class PatternUtils:

    @staticmethod
    def contains_assignment(line: str) -> bool:
        """Check if a line contains an assignment."""
        return '=' in line and not line.lstrip().startswith('#')

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        """Apply consistent spacing around assignment operator."""
        parts = line.split('=')
        if len(parts) != 2:
            return line

        var, value = parts
        var = var.rstrip()
        value = value.lstrip()

        if use_spaces:
            return f'{var} = {value}'
        else:
            return f'{var}={value}'

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        """Format a target colon line."""
        line = line.strip()
        if not line.endswith(':'):
            return None

        target = line[:-1].rstrip()
        colon = ':'

        if space_before:
            target += ' '
        if space_after:
            colon = ' :'

        return target + colon

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        """Format a pattern rule line."""
        parts = line.split(':')
        if len(parts) != 2:
            return None

        target = parts[0].rstrip()
        dependencies = parts[1].lstrip()

        colon = ':'
        if space_after_colon:
            colon += ' '

        return f'{target}{colon}{dependencies}'

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        """Check if a line is a conditional directive."""
        line = line.strip()
        return line.startswith(('ifeq', 'ifneq', 'ifdef', 'ifndef', 'else', 'endif'))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        """Get the conditional indent level of a line."""
        line = line.strip()
        if line.startswith('ifeq') or line.startswith('ifneq') or line.startswith('ifdef') or line.startswith('ifndef'):
            return 1
        elif line.startswith('else'):
            return 0
        elif line.startswith('endif'):
            return -1
        else:
            return 0
