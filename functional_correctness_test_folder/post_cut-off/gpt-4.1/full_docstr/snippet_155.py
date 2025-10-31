
import re
from typing import Optional


class PatternUtils:
    '''Common pattern matching utilities used across formatting rules.'''

    # Assignment operators in Makefiles: =, :=, ?=, +=
    ASSIGNMENT_RE = re.compile(r'(?<![<\w])\s*([:+?]?=)\s*')
    # Target definition: target: deps
    TARGET_COLON_RE = re.compile(r'^([^\s:=][^:=]*?)(\s*):(\s*)(.*)$')
    # Pattern rule: %.o: %.c
    PATTERN_RULE_RE = re.compile(r'^([^\s:=][^:=%]*%[^:=]*)(\s*):(\s*)(.*)$')
    # Conditional directives
    CONDITIONALS = (
        'ifeq', 'ifneq', 'ifdef', 'ifndef', 'else', 'endif'
    )
    CONDITIONAL_RE = re.compile(r'^\s*(ifeq|ifneq|ifdef|ifndef|else|endif)\b')

    @staticmethod
    def contains_assignment(line: str) -> bool:
        '''
        Check if line contains an assignment operator.
        '''
        # Ignore lines that are comments or empty
        line = line.strip()
        if not line or line.startswith('#'):
            return False
        # Look for assignment operator not in a recipe line (not indented with tab)
        if line.startswith('\t'):
            return False
        # Find assignment operator
        return bool(PatternUtils.ASSIGNMENT_RE.search(line))

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        '''
        Apply consistent spacing around assignment operators.
        '''
        def replacer(match):
            op = match.group(1)
            if use_spaces:
                return f' {op} '
            else:
                return op
        # Only replace the first assignment operator in the line
        new_line, n = PatternUtils.ASSIGNMENT_RE.subn(replacer, line, count=1)
        return new_line

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        '''
        Format colon spacing in target definitions.
        '''
        m = PatternUtils.TARGET_COLON_RE.match(line)
        if not m:
            return None
        target, before_colon, after_colon, rest = m.groups()
        new_before = ' ' if space_before else ''
        new_after = ' ' if space_after else ''
        formatted = f"{target}{new_before}:{new_after}{rest}"
        if formatted == line:
            return None
        return formatted

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        '''
        Format spacing in pattern rules.
        '''
        m = PatternUtils.PATTERN_RULE_RE.match(line)
        if not m:
            return None
        pattern, before_colon, after_colon, rest = m.groups()
        new_after = ' ' if space_after_colon else ''
        formatted = f"{pattern}:{new_after}{rest}"
        if formatted == line:
            return None
        return formatted

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        '''
        Check if line is a conditional directive.
        '''
        line = line.strip()
        if not line or line.startswith('#'):
            return False
        return bool(PatternUtils.CONDITIONAL_RE.match(line))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        '''
        Get the appropriate indentation level for conditional directives.
        '''
        # Simple rule: 0 for 'ifeq', 'ifneq', 'ifdef', 'ifndef', 'endif', 'else'
        # You can customize this as needed. Here, we return 0 for all.
        # If you want to indent nested conditionals, you would need context.
        return 0
