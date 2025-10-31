
import re
from typing import Optional


class PatternUtils:
    '''Common pattern matching utilities used across formatting rules.'''

    # Regular expression patterns for assignment operators in Makefiles
    _assignment_ops = re.compile(r'(?<![!<>=])([?+]?=|:=|?=|<|>|!|=)')
    _assignment_ops_no_space = re.compile(r'(?<![!<>=])([?+]?=|:=|?=|<|>|!|=)')

    @staticmethod
    def contains_assignment(line: str) -> bool:
        """
        Check if line contains an assignment operator.
        """
        return bool(PatternUtils._assignment_ops.search(line))

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        """
        Apply consistent spacing around assignment operators.
        """
        def repl(match):
            op = match.group(1)
            if use_spaces:
                return f' {op} '
            else:
                return op

        # Replace only the first occurrence to avoid affecting other parts
        return PatternUtils._assignment_ops.sub(repl, line, count=1)

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        """
        Format colon spacing in target definitions.
        """
        # Find the first colon that is not part of a pattern rule (i.e., not preceded by a %)
        match = re.search(r'(?<!%)\s*:\s*', line)
        if not match:
            return None

        start, end = match.span()
        before = line[:start]
        after = line[end:]

        # Build new colon segment
        colon = ':'
        if space_before:
            colon = f' {colon}'
        if space_after:
            colon = f'{colon} '

        new_line = before + colon + after
        if new_line == line:
            return None
        return new_line

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        """
        Format spacing in pattern rules.
        """
        # Pattern rules contain a % before the colon
        match = re.search(r'(?<=%)\s*:\s*', line)
        if not match:
            return None

        start, end = match.span()
        before = line[:start]
        after = line[end:]

        colon = ':'
        if space_after_colon:
            colon = f'{colon} '

        new_line = before + colon + after
        if new_line == line:
            return None
        return new_line

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        """
        Check if line is a conditional directive.
        """
        stripped = line.strip()
        return stripped.startswith(('ifeq', 'ifneq', 'ifdef', 'ifndef', 'else', 'endif'))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        """
        Get the appropriate indentation level for conditional directives.
        """
        stripped = line.strip()
        if stripped.startswith(('ifeq', 'ifneq', 'ifdef', 'ifndef')):
            return 4
        if stripped.startswith(('else', 'endif')):
            return 0
        return 0
