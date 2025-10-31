
import re
from typing import Optional


class PatternUtils:

    @staticmethod
    def contains_assignment(line: str) -> bool:
        # Detects =, :=, ?=, +=, !=, but not == or inside strings
        # Exclude lines that are comments or empty
        line = line.strip()
        if not line or line.startswith('#'):
            return False
        # Exclude == (equality)
        # Match variable assignment at start of line (allow spaces)
        # e.g. VAR = value, VAR := value, VAR ?= value, VAR += value, VAR != value
        return bool(re.match(r'^[^#\n]*\b\w+\s*(\?|:|\+|!)?=\s*[^=]', line))

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        # Normalize spacing around assignment operators (=, :=, ?=, +=, !=)
        def replacer(match):
            var = match.group(1)
            op = match.group(2)
            if use_spaces:
                return f"{var} {op} "
            else:
                return f"{var}{op}"
        # Only replace the first assignment operator in the line
        pattern = r'^(\s*\w+)\s*(\?|:|\+|!)?=\s*'
        return re.sub(pattern, replacer, line, count=1)

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        '''
        Format colon spacing in target definitions.
        '''
        # Target: deps
        # Pattern: ^target\s*:.*$
        m = re.match(r'^(\s*\S.*?)(\s*):(\s*)(.*)$', line)
        if not m:
            return None
        before = m.group(1)
        after = m.group(4)
        colon = ':'
        new_line = before
        if space_before:
            new_line += ' '
        new_line += colon
        if space_after:
            new_line += ' '
        new_line += after
        if new_line == line:
            return None
        return new_line

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        # Pattern rule: %.o: %.c
        # Only match lines with % and a colon
        m = re.match(r'^(\s*[^#\n]*%[^:]*)(\s*):(\s*)(.*)$', line)
        if not m:
            return None
        before = m.group(1)
        after = m.group(4)
        colon = ':'
        new_line = before + colon
        if space_after_colon:
            new_line += ' '
        new_line += after
        if new_line == line:
            return None
        return new_line

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        # Recognize ifeq, ifneq, ifdef, ifndef, else, endif (case-insensitive, at start)
        return bool(re.match(r'^\s*(ifeq|ifneq|ifdef|ifndef|else|endif)\b', line, re.IGNORECASE))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        '''
        Get the appropriate indentation level for conditional directives.
        '''
        # Common convention: 0 for if*, 2 for else, 0 for endif
        # But let's use 2 spaces for else, 0 for others
        line = line.strip().lower()
        if line.startswith('else'):
            return 2
        return 0
