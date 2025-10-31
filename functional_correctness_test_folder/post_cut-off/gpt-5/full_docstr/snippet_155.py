from typing import Optional
import re


class PatternUtils:
    '''Common pattern matching utilities used across formatting rules.'''
    ASSIGN_OP_RE = re.compile(
        r'(^|[ \t])([A-Za-z0-9_][A-Za-z0-9_.-]*)[ \t]*(\+?=|\?=|:=|=)')
    CONDITIONAL_RE = re.compile(
        r'^[ \t]*(ifeq|ifneq|ifdef|ifndef|else|endif)\b', re.IGNORECASE)

    @staticmethod
    def contains_assignment(line: str) -> bool:
        line_stripped = line.lstrip()
        if not line_stripped or line_stripped.startswith('#') or line_stripped.startswith('\t'):
            return False
        m = PatternUtils.ASSIGN_OP_RE.search(line)
        return m is not None

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        # Don't touch recipe lines or comments
        line_stripped = line.lstrip()
        if line_stripped.startswith('#') or line_stripped.startswith('\t'):
            return line

        m = re.match(
            r'^([ \t]*)([A-Za-z0-9_][A-Za-z0-9_.-]*)([ \t]*)(\+?=|\?=|:=|=)([ \t]*)(.*)$', line)
        if not m:
            return line

        lead, var, _ws1, op, _ws2, val = m.groups()
        val = val.rstrip()
        if use_spaces:
            formatted = f'{lead}{var} {op} {val}'
        else:
            formatted = f'{lead}{var}{op}{val}'
        return formatted

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        s = line
        ls = s.lstrip()
        if not ls or ls.startswith('#') or ls.startswith('\t'):
            return None

        # Find earliest colon (single or double)
        colon_match = re.search(r'::|:', s)
        if not colon_match:
            return None
        cstart, cend = colon_match.span()
        colon_token = s[cstart:cend]

        # If any assignment operator occurs before the colon, skip
        assign_match = re.search(r'\+?=|\?=|:=|=', s)
        if assign_match and assign_match.start() < cstart:
            return None

        # Avoid pattern rules here (handled by format_pattern_rule)
        if '%' in s[:cstart]:
            return None

        left = s[:cstart].rstrip()
        right = s[cend:].lstrip()

        new_left = left + \
            (' ' if space_before and (not left.endswith(' ')) else '')
        new_right = (' ' if space_after else '') + right

        new_line = new_left + colon_token + new_right
        return None if new_line == line else new_line

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        s = line
        ls = s.lstrip()
        if not ls or ls.startswith('#') or ls.startswith('\t'):
            return None

        colon_match = re.search(r'::|:', s)
        if not colon_match:
            return None
        cstart, cend = colon_match.span()
        colon_token = s[cstart:cend]

        # Must be a pattern rule: '%' before colon
        if '%' not in s[:cstart]:
            return None

        # If any assignment operator occurs before the colon, skip
        assign_match = re.search(r'\+?=|\?=|:=|=', s)
        if assign_match and assign_match.start() < cstart:
            return None

        left = s[:cstart].rstrip()
        right = s[cend:].lstrip()

        # No space before colon in pattern rules
        new_left = left
        new_right = (' ' if space_after_colon else '') + right

        new_line = new_left + colon_token + new_right
        return None if new_line == line else new_line

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        return PatternUtils.CONDITIONAL_RE.match(line) is not None

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        # Conditional directives (ifeq/ifneq/ifdef/ifndef/else/endif) are not indented.
        return 0
