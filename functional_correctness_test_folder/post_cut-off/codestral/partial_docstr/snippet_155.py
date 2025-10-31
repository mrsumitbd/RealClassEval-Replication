
from typing import Optional


class PatternUtils:

    @staticmethod
    def contains_assignment(line: str) -> bool:
        return '=' in line

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        if '=' in line:
            parts = line.split('=', 1)
            if use_spaces:
                return f"{parts[0].strip()} = {parts[1].strip()}"
            else:
                return f"{parts[0].strip()}={parts[1].strip()}"
        return line

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        if ':' in line:
            parts = line.split(':', 1)
            if space_before and space_after:
                return f"{parts[0].strip()} : {parts[1].strip()}"
            elif space_before:
                return f"{parts[0].strip()} :{parts[1].strip()}"
            elif space_after:
                return f"{parts[0].strip()}: {parts[1].strip()}"
            else:
                return f"{parts[0].strip()}:{parts[1].strip()}"
        return None

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        if ':' in line:
            parts = line.split(':', 1)
            if space_after_colon:
                return f"{parts[0].strip()}: {parts[1].strip()}"
            else:
                return f"{parts[0].strip()}:{parts[1].strip()}"
        return None

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        return line.strip().startswith(('if', 'else', 'endif'))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        if line.strip().startswith('if'):
            return 4
        elif line.strip().startswith('else'):
            return 4
        elif line.strip().startswith('endif'):
            return 0
        return 0
