from typing import Optional
import re


class PatternUtils:
    '''Common pattern matching utilities used across formatting rules.'''

    ASSIGNMENT_OP_RE = re.compile(r'(?:\+|:|\?|!){0,2}=')
    COMMENT_SPLIT_RE = re.compile(r'(?<!\\)#')

    @staticmethod
    def _split_comment(line: str):
        if not line:
            return '', ''
        m = PatternUtils.COMMENT_SPLIT_RE.search(line)
        if not m:
            return line, ''
        idx = m.start()
        return line[:idx], line[idx:]

    @staticmethod
    def _is_recipe_line(line: str) -> bool:
        if not line:
            return False
        # Consider leading spaces before a TAB as a recipe line as well.
        stripped = line.lstrip(' ')
        return stripped.startswith('\t')

    @staticmethod
    def _find_assignment_operator(code: str) -> Optional[re.Match]:
        # Find the first assignment operator that is preceded by a plausible variable token.
        for m in PatternUtils.ASSIGNMENT_OP_RE.finditer(code):
            op_start = m.start()
            i = op_start - 1
            # Skip whitespace before operator
            while i >= 0 and code[i].isspace():
                i -= 1
            if i < 0:
                continue
            # Handle $(var) variable name
            if code[i] == ')':
                # Walk back to find matching '$('
                depth = 1
                j = i - 1
                while j >= 0:
                    c = code[j]
                    if c == ')':
                        depth += 1
                    elif c == '(':
                        depth -= 1
                        if depth == 0:
                            # Check for '$(' just before '('
                            if j - 1 >= 0 and code[j - 1] == '$':
                                var_start = j - 1
                                # Accept this as variable token
                                return m
                            else:
                                break
                    j -= 1
                # If not matched, continue scanning
                continue
            # Handle bare variable names: [A-Za-z0-9_.-]+ possibly preceded by keywords (ignored)
            allowed = set(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-")
            j = i
            while j >= 0 and code[j] in allowed:
                j -= 1
            # Ensure we captured at least one character
            if j == i:
                continue
            # It's a plausible variable name
            return m
        return None

    @staticmethod
    def contains_assignment(line: str) -> bool:
        '''
        Check if line contains an assignment operator.
        Args:
            line: The line to check
        Returns:
            True if line contains assignment operators
        '''
        if not line or PatternUtils._is_recipe_line(line) or PatternUtils.is_conditional_directive(line):
            return False
        code, _ = PatternUtils._split_comment(line)
        if not code.strip():
            return False
        return PatternUtils._find_assignment_operator(code) is not None

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
        if not line or PatternUtils._is_recipe_line(line) or PatternUtils.is_conditional_directive(line):
            return line

        code, comment = PatternUtils._split_comment(line)
        if not code:
            return line

        m = PatternUtils._find_assignment_operator(code)
        if not m:
            return line

        op = m.group(0)
        op_start = m.start()
        op_end = m.end()

        # Find the end of the variable token (position just before whitespace before op)
        i = op_start - 1
        while i >= 0 and code[i].isspace():
            i -= 1
        if i < 0:
            return line

        # Determine start of variable token
        if code[i] == ')':
            depth = 1
            j = i - 1
            var_start = None
            while j >= 0:
                c = code[j]
                if c == ')':
                    depth += 1
                elif c == '(':
                    depth -= 1
                    if depth == 0:
                        if j - 1 >= 0 and code[j - 1] == '$':
                            var_start = j - 1
                        break
                j -= 1
            if var_start is None:
                return line
            lhs_end = i + 1
            lhs_start = var_start
        else:
            allowed = set(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-")
            j = i
            while j >= 0 and code[j] in allowed:
                j -= 1
            lhs_start = j + 1
            lhs_end = i + 1

        # Build formatted string
        left_prefix = code[:lhs_end].rstrip()
        right_suffix = code[op_end:].lstrip()

        if use_spaces:
            middle = f' {op} '
        else:
            middle = op

        formatted = f'{left_prefix}{middle}{right_suffix}{comment}'
        return formatted

    @staticmethod
    def _find_top_level_colon(code: str) -> Optional[tuple]:
        # Returns (index, token) where token is ':' or '::'
        depth = 0
        i = 0
        code_len = len(code)
        while i < code_len:
            c = code[i]
            if c == '(':
                depth += 1
            elif c == ')':
                if depth > 0:
                    depth -= 1
            elif c == ':' and depth == 0:
                # If this is ':=' treat as assignment colon, not a target colon
                if i + 1 < code_len and code[i + 1] == '=':
                    i += 1
                    continue
                # Handle double-colon '::'
                if i + 1 < code_len and code[i + 1] == ':':
                    return i, '::'
                return i, ':'
            i += 1
        return None

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
        if not line or PatternUtils._is_recipe_line(line) or PatternUtils.is_conditional_directive(line):
            return None

        code, comment = PatternUtils._split_comment(line)
        if not code.strip():
            return None

        # If there is an assignment before a colon, treat as assignment line.
        m = PatternUtils._find_assignment_operator(code)
        assignment_index = m.start() if m else None

        found = PatternUtils._find_top_level_colon(code)
        if not found:
            return None
        colon_index, token = found

        if assignment_index is not None and assignment_index < colon_index:
            return None

        left = code[:colon_index]
        right = code[colon_index + len(token):]

        left_fmt = left.rstrip()
        right_fmt = right.lstrip()

        before = ' ' if space_before else ''
        after = ' ' if space_after else ''

        new_code = f'{left_fmt}{before}{token}{after}{right_fmt}'
        new_line = new_code + comment

        return None if new_line == line else new_line

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
        if not line or PatternUtils._is_recipe_line(line) or PatternUtils.is_conditional_directive(line):
            return None

        code, _ = PatternUtils._split_comment(line)
        found = PatternUtils._find_top_level_colon(code)
        if not found:
            return None
        colon_index, _ = found

        # Determine if left side contains a '%' (pattern)
        left_side = code[:colon_index]
        if '%' not in left_side:
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
        s = line.lstrip()
        if s.startswith('#'):
            return False
        keywords = (
            'ifeq', 'ifneq', 'ifdef', 'ifndef',
            'else ifeq', 'else ifneq', 'else ifdef', 'else ifndef',
            'else', 'endif'
        )
        s_lower = s.lower()
        for kw in keywords:
            if s_lower.startswith(kw):
                # Ensure whole word match
                if len(s_lower) == len(kw) or s_lower[len(kw)].isspace() or s_lower[len(kw)] in '()':
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
        # For make conditionals, common style is no indentation for directive lines.
        return 0
