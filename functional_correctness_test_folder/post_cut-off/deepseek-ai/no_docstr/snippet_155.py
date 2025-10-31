
from typing import Optional


class PatternUtils:

    @staticmethod
    def contains_assignment(line: str) -> bool:
        return '=' in line

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        if '=' not in line:
            return line
        parts = line.split('=', 1)
        left, right = parts[0].rstrip(), parts[1].lstrip()
        if use_spaces:
            return f"{left} = {right}"
        else:
            return f"{left}={right}"

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        if ':' not in line:
            return None
        parts = line.split(':', 1)
        left, right = parts[0].rstrip(), parts[1].lstrip()
        result = left
        if space_before:
            result += ' '
        result += ':'
        if space_after:
            result += ' '
        result += right
        return result

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        if ':' not in line:
            return None
        parts = line.split(':', 1)
        left, right = parts[0].rstrip(), parts[1].lstrip()
        if space_after_colon:
            return f"{left}: {right}"
        else:
            return f"{left}:{right}"

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        stripped = line.strip()
        return stripped.startswith(('#if', '#elif', '#else', '#endif'))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        stripped = line.lstrip()
        return len(line) - len(stripped)
