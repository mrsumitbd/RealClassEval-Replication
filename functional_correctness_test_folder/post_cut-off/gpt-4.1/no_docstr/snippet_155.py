
import re
from typing import Optional


class PatternUtils:

    @staticmethod
    def contains_assignment(line: str) -> bool:
        # Detects variable assignments like VAR = value, VAR := value, VAR += value, VAR ?= value
        # Not inside comments, not inside recipe lines (starting with tab)
        if line.lstrip().startswith('#') or line.startswith('\t'):
            return False
        # Match: identifier, optional spaces, assignment operator, not inside a rule (target: ...)
        assignment_pattern = r'^[A-Za-z_][A-Za-z0-9_]*\s*(\?|:)?\+?='
        return re.match(assignment_pattern, line.strip()) is not None

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        # Normalize spacing around assignment operators (=, :=, +=, ?=)
        def replacer(match):
            var = match.group(1)
            op = match.group(2)
            if use_spaces:
                return f"{var} {op} "
            else:
                return f"{var}{op}"
        pattern = r'^([A-Za-z_][A-Za-z0-9_]*)\s*(\?|:)?\+?='
        return re.sub(pattern, replacer, line, count=1)

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        # Format target: dependencies lines (not variable assignments)
        # e.g. "foo:bar" -> "foo: bar"
        if ':' not in line:
            return None
        # Exclude variable assignments
        if PatternUtils.contains_assignment(line):
            return None
        # Only process the first colon
        m = re.match(r'^([^\s:][^:]*)\s*:\s*(.*)$', line)
        if not m:
            return None
        target, rest = m.group(1), m.group(2)
        before = ' ' if space_before else ''
        after = ' ' if space_after else ''
        return f"{target}{before}:{after}{rest}"

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        # Format pattern rules: %.o: %.c or %.o: %.c %.h
        # Only process if line contains a % and a colon, and is not an assignment
        if '%' not in line or ':' not in line:
            return None
        if PatternUtils.contains_assignment(line):
            return None
        m = re.match(r'^([^\s:][^:]*)\s*:\s*(.*)$', line)
        if not m:
            return None
        target, rest = m.group(1), m.group(2)
        after = ' ' if space_after_colon else ''
        return f"{target}:{after}{rest}"

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        # Detects ifeq, ifneq, ifdef, ifndef, else, endif at start of line (ignoring leading spaces)
        cond_pattern = r'^\s*(ifeq|ifneq|ifdef|ifndef|else|endif)\b'
        return re.match(cond_pattern, line) is not None

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        # Returns the number of leading spaces (indentation level) for conditional directives
        if not PatternUtils.is_conditional_directive(line):
            return 0
        return len(line) - len(line.lstrip(' '))
