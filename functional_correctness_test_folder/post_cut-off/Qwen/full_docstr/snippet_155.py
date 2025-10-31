
import re
from typing import Optional


class PatternUtils:
    '''Common pattern matching utilities used across formatting rules.'''
    @staticmethod
    def contains_assignment(line: str) -> bool:
        return '=' in line

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        if use_spaces:
            return re.sub(r'\s*=\s*', ' = ', line)
        else:
            return re.sub(r'\s*=\s*', '=', line)

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        pattern = r'(?<!:):' if space_before else r':'
        replacement = ' :' if space_before and space_after else ':' if not space_before and not space_after else ': '
        new_line = re.sub(pattern, replacement, line)
        return new_line if new_line != line else None

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        pattern = r':'
        replacement = ': ' if space_after_colon else ':'
        new_line = re.sub(pattern, replacement, line)
        return new_line if new_line != line else None

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        return line.strip().startswith(('if', 'elif', 'else', 'try', 'except', 'finally', 'for', 'while', 'with'))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        stripped_line = line.lstrip()
        return len(line) - len(stripped_line)
