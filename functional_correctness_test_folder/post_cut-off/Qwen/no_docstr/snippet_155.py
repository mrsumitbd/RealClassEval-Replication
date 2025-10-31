
from typing import Optional


class PatternUtils:

    @staticmethod
    def contains_assignment(line: str) -> bool:
        return '=' in line and not line.strip().startswith('#')

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        if not PatternUtils.contains_assignment(line):
            return line
        if use_spaces:
            return ' = '.join(part.strip() for part in line.split('=', 1))
        else:
            return '='.join(part.strip() for part in line.split('=', 1))

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        if ':' not in line or PatternUtils.contains_assignment(line):
            return None
        parts = line.split(':', 1)
        if space_before:
            parts[0] = parts[0].rstrip() + ' '
        if space_after:
            parts[1] = ' ' + parts[1].lstrip()
        else:
            parts[1] = parts[1].lstrip()
        return ':'.join(parts)

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        if ':' not in line or PatternUtils.contains_assignment(line):
            return None
        parts = line.split(':', 1)
        if space_after_colon:
            parts[1] = ' ' + parts[1].lstrip()
        else:
            parts[1] = parts[1].lstrip()
        return ':'.join(parts)

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        return line.strip().startswith(('if', 'elif', 'else', 'ifdef', 'ifndef', 'endif'))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        stripped_line = line.lstrip()
        return len(line) - len(stripped_line)
