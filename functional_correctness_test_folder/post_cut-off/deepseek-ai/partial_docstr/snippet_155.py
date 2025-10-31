
from typing import Optional


class PatternUtils:

    @staticmethod
    def contains_assignment(line: str) -> bool:
        return '=' in line

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        if '=' in line:
            if use_spaces:
                line = line.replace('=', ' = ')
                line = ' '.join(line.split())  # Normalize spacing
            else:
                line = line.replace(' = ', '=').replace(
                    '= ', '=').replace(' =', '=')
        return line

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        if ':' not in line:
            return None

        parts = line.split(':', 1)
        before = parts[0].rstrip()
        after = parts[1].lstrip()

        new_before = before + ' ' if space_before else before
        new_after = ' ' + after if space_after else after

        new_line = f"{new_before}:{new_after}"
        return new_line if new_line != line else None

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str:
        if ':' not in line:
            return None

        parts = line.split(':', 1)
        before = parts[0].rstrip()
        after = parts[1].lstrip()

        new_after = ' ' + after if space_after_colon else after
        new_line = f"{before}:{new_after}"
        return new_line if new_line != line else None

    @ staticmethod
    def is_conditional_directive(line: str) -> bool:
        stripped = line.strip()
        return stripped.startswith(('ifdef', 'ifndef', 'ifeq', 'ifneq', 'else', 'endif'))

    @ staticmethod
    def get_conditional_indent_level(line: str) -> int:
        stripped = line.lstrip()
        return len(line) - len(stripped)
