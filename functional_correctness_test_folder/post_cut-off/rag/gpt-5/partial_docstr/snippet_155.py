from typing import Optional
import re


class PatternUtils:
    '''Common pattern matching utilities used across formatting rules.'''

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
    def contains_assignment(line: str) -> bool:
        '''
        Check if line contains an assignment operator.
        Args:
            line: The line to check
        Returns:
            True if line contains assignment operators
        '''
        if not line:
            return False
        stripped = line.lstrip()
        if not stripped or stripped.startswith('#'):
            return False
        # Skip recipe lines (make commands)
        if stripped.startswith('\t'):
            return False

        code, _ = PatternUtils._split_comment(stripped)
        # Ignore define/endef blocks
        if code.lstrip().startswith(('define ', 'endef')):
            return False

        # Assignment operators in make
        ops = (':=', '+=', '?=', '!=', '=')
        # Find any operator occurrence
        for op in ops:
            idx = code.find(op)
            if idx != -1:
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

        # Preserve original leading indentation
        leading_ws_len = len(line) - len(line.lstrip(' '))
        leading_ws = line[:leading_ws_len]
        rest = line[leading_ws_len:]

        # Don't alter comments or recipe lines
        if rest.startswith('#') or rest.startswith('\t'):
            return line

        code, comment = PatternUtils._split_comment(rest)

        ops = (':=', '+=', '?=', '!=', '=')

        # Find earliest operator occurrence
        op_pos = None
        op_found = None
        for op in ops:
            pos = code.find(op)
            if pos != -1 and (op_pos is None or pos < op_pos):
                op_pos = pos
                op_found = op

        if op_pos is None:
            return line

        lhs = code[:op_pos].rstrip()
        rhs = code[op_pos + len(op_found):].lstrip(
        ) if use_spaces else code[op_pos + len(op_found):].lstrip()

        if use_spaces:
            formatted_code = f'{lhs} {op_found} {rhs}'
        else:
            formatted_code = f'{lhs}{op_found}{rhs}'

        new_line = leading_ws + formatted_code + comment
        return new_line

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
        if not line or ':' not in line:
            return None

        stripped = line.lstrip()
        if stripped.startswith('#') or stripped.startswith('\t'):
            return None

        # Do not modify lines that are variable assignments with ':='
        if PatternUtils.contains_assignment(line):
            # Could still be target-specific variable assignment "target: VAR = val"
            # We still may want to format the colon before the assignment.
            pass

        s = line
        # Find first ':' that is not part of ':='
        colon_idx = None
        colons_len = 1
        for i, ch in enumerate(s):
            if ch != ':':
                continue
            # skip ':='
            if i + 1 < len(s) and s[i + 1] == '=':
                continue
            # detect '::'
            if i + 1 < len(s) and s[i + 1] == ':':
                colon_idx = i
                colons_len = 2
                break
            colon_idx = i
            colons_len = 1
            break

        if colon_idx is None:
            return None

        left = s[:colon_idx]
        right = s[colon_idx + colons_len:]

        left_fmt = left.rstrip()
        right_fmt = right.lstrip()

        before = ' ' if space_before and left_fmt else ''
        after = ' ' if space_after and (right_fmt != '' or right != '') else ''

        new_line = f'{left_fmt}{before}{"::" if colons_len == 2 else ":"}{after}{right_fmt}'

        if new_line == line:
            return None
        return new_line

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
        if not line or ':' not in line:
            return None

        stripped = line.lstrip()
        if stripped.startswith('#') or stripped.startswith('\t'):
            return None

        # Identify colon separating target and prerequisites (not ':=')
        s = line
        colon_idx = None
        colons_len = 1
        for i, ch in enumerate(s):
            if ch != ':':
                continue
            if i + 1 < len(s) and s[i + 1] == '=':
                continue
            if i + 1 < len(s) and s[i + 1] == ':':
                colon_idx = i
                colons_len = 2
                break
            colon_idx = i
            colons_len = 1
            break

        if colon_idx is None:
            return None

        left = s[:colon_idx]
        # Determine if this looks like a pattern or suffix rule
        left_stripped = left.strip()
        is_pattern = ('%' in left_stripped) or left_stripped.startswith('.')

        if not is_pattern:
            return None

        right = s[colon_idx + colons_len:]
        left_fmt = left.rstrip()
        right_fmt = right.lstrip()

        after = ' ' if space_after_colon and (
            right_fmt != '' or right != '') else ''
        new_line = f'{left_fmt}{"::" if colons_len == 2 else ":"}{after}{right_fmt}'

        if new_line == line:
            return None
        return new_line

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
        s = line.strip()
        if not s or s.startswith('#'):
            return False

        # Normalize multiple spaces
        token = s.split(None, 1)[0]
        if token in ('ifeq', 'ifneq', 'ifdef', 'ifndef', 'else', 'endif'):
            return True
        if s.startswith('else if'):
            return True
        return False

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        '''
        Get the appropriate indentation level for conditional directives.
        Args:
            line: The conditional directive line
        Returns:
            Number of spaces for indentation
        '''
        # By default, conditional directive lines are not indented.
        # Body lines within conditionals should be indented by the caller.
        return 0
