
class PatternUtils:

    @staticmethod
    def contains_assignment(line: str) -> bool:
        return '=' in line

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        if '=' in line:
            parts = line.split('=')
            if use_spaces:
                return ' = '.join(parts)
            else:
                return '='.join(parts)
        return line

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        if ':' in line:
            parts = line.split(':')
            if space_before and space_after:
                return ': '.join(parts)
            elif space_before:
                return ' :'.join(parts)
            elif space_after:
                return ': '.join(parts)
            else:
                return ':'.join(parts)
        return None

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        if ':' in line:
            parts = line.split(':')
            if space_after_colon:
                return ': '.join(parts)
            else:
                return ':'.join(parts)
        return None

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        return line.strip().startswith(('if', 'else', 'elif'))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        if PatternUtils.is_conditional_directive(line):
            return line.find(line.strip())
        return 0
