from typing import Optional
import re


class PatternUtils:
    '''Common pattern matching utilities used across formatting rules.'''

    _ASSIGNMENT_PATTERN = re.compile(r'(\+=|\?=|:=|!=|=(?!=))')

    @staticmethod
    def _split_comment(line: str):
        escaped = False
        for i, ch in enumerate(line):
            if ch == '\\' and not escaped:
                escaped = True
                continue
            if ch == '#' and not escaped:
                return line[:i], line[i:]
            escaped = False
        return line, ''

    @staticmethod
    def _find_assignment(code: str):
        match = PatternUtils._ASSIGNMENT_PATTERN.search(code)
        if not match:
            return None
        pre = code[:match.start()]
        # ensure there is some non-whitespace before the operator
        if pre.strip() == '':
            return None
        return match

    @staticmethod
    def contains_assignment(line: str) -> bool:
        '''
        Check if line contains an assignment operator.
        Args:
            line: The line to check
        Returns:
            True if line contains assignment operators
        '''
        if not line or line.lstrip().startswith('#') or line.startswith('\t'):
            return False
        code, _comment = PatternUtils._split_comment(line)
        if PatternUtils._find_assignment(code):
            return True
        # Also check for assignment after a target colon
        if ':' in code:
            after = code.split(':', 1)[1]
            if PatternUtils._find_assignment(after):
                return True
        return False

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        '''
        Apply consistent spacing around assignment operators.
        Args:
            line: The line to format
            use_spaces: Whether to use spaces around operators
        Returns:
            The formatted line
        '''
        if not line:
            return line
        code, comment = PatternUtils._split_comment(line)

        m = PatternUtils._find_assignment(code)
        # If not found in the whole code, try only after the first colon (target-specific vars)
        if not m and ':' in code:
            prefix, rest = code.split(':', 1)
            m = PatternUtils._find_assignment(rest)
            if m:
                start, end = m.span()
                lhs = rest[:start].rstrip()
                rhs = rest[end:].lstrip()
                op = m.group(1)
                mid = f' {op} ' if use_spaces else op
                new_rest = lhs + mid + rhs
                new_code = prefix + ':' + new_rest
                return new_code + comment

        if not m:
            return line

        start, end = m.span()
        lhs = code[:start].rstrip()
        rhs = code[end:].lstrip()
        op = m.group(1)

        mid = f' {op} ' if use_spaces else op
        new_code = lhs + mid + rhs
        return new_code + comment

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        '''
        Format colon spacing in target definitions.
        Args:
            line: The line to format
            space_before: Whether to add space before colon
            space_after: Whether to add space after colon
        Returns:
            Formatted line or None if no changes needed
        '''
        if not line or line.startswith('\t') or line.lstrip().startswith('#'):
            return None

        code, comment = PatternUtils._split_comment(line)
        if ':' not in code:
            return None

        # Ensure the colon is part of a target definition and not after an assignment
        m_assign = PatternUtils._find_assignment(code)
        colon_index = code.find(':')
        if m_assign and colon_index > m_assign.start():
            return None

        left = code[:colon_index]
        # Handle single vs double colon rules
        colons = ':'
        right_start = colon_index + 1
        if right_start < len(code) and code[right_start] == ':':
            colons = '::'
            right_start += 1

        right = code[right_start:]

        new_left = left.rstrip()
        if space_before and new_left and not new_left.endswith(' '):
            new_left += ' '

        new_right = right.lstrip()
        if space_after and new_right:
            new_right = ' ' + new_right

        new_code = f'{new_left}{colons}{new_right}'
        result = new_code + comment

        if result == line:
            return None
        return result

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        '''
        Format spacing in pattern rules.
        Args:
            line: The line to format
            space_after_colon: Whether to add space after colon
        Returns:
            Formatted line or None if no changes needed
        '''
        if not line or line.startswith('\t') or line.lstrip().startswith('#'):
            return None

        code, _comment = PatternUtils._split_comment(line)
        if ':' not in code:
            return None

        # Pattern rules typically contain '%' on either side of colon
        if '%' not in code:
            return None

        return PatternUtils.format_target_colon(line, space_before=False, space_after=space_after_colon)

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        '''
        Check if line is a conditional directive.
        Args:
            line: The line to check
        Returns:
            True if this is a conditional directive
        '''
        if not line:
            return False
        if line.startswith('\t'):
            return False
        stripped = line.lstrip()
        if stripped.startswith('#'):
            return False
        pattern = re.compile(
            r'^(?:ifdef|ifndef|ifeq|ifneq|else(?:\s+(?:ifdef|ifndef|ifeq|ifneq))?|endif)\b')
        return bool(pattern.match(stripped))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        '''
        Get the appropriate indentation level for conditional directives.
        Args:
            line: The conditional directive line
        Returns:
            Number of spaces for indentation
        '''
        # Keep conditional directives at base indentation.
        return 0
