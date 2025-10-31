import re
from typing import Optional


class PatternUtils:
    '''Common pattern matching utilities used across formatting rules.'''

    @staticmethod
    def contains_assignment(line: str) -> bool:
        '''
        Check if line contains an assignment operator.
        Args:
            line: The line to check
        Returns:
            True if line contains assignment operators
        '''
        # Match =, :=, ?=, +=, !=, but not == or inside strings/comments
        # Exclude ==, >=, <=, != (except for make's !=)
        # We'll match only if = is not surrounded by another =
        return bool(re.search(r'(?<![<>=!])\s*([:+?]?=)\s*(?![=])', line))

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
        # Only operate on the first assignment operator in the line
        def replacer(match):
            op = match.group(1)
            if use_spaces:
                return f' {op} '
            else:
                return op
        # Only replace if it's not ==, >=, <=, != (except for make's !=)
        pattern = r'(?<![<>=!])\s*([:+?]?=)\s*(?![=])'
        return re.sub(pattern, replacer, line, count=1)

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
        # Only operate if line looks like a target definition: target: dep
        # Don't match pattern rules (%.o: %.c)
        # Only match the first colon not inside a variable assignment
        # Heuristic: if line contains = before :, skip
        eq_pos = line.find('=')
        colon_pos = line.find(':')
        if colon_pos == -1 or (eq_pos != -1 and eq_pos < colon_pos):
            return None
        # Don't match double colon
        if line[colon_pos:colon_pos+2] == '::':
            return None
        # Only operate if not already correct
        before = ' ' if space_before else ''
        after = ' ' if space_after else ''
        # Remove all spaces around the first colon
        new_line = re.sub(r'\s*:\s*', f'{before}:{after}', line, count=1)
        if new_line != line:
            return new_line
        return None

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
        # Pattern rule: %.o: %.c or %.o: %.c %.h
        # Only operate if line starts with % or contains % before colon
        m = re.match(r'^([^\s=]+%[^\s=]*)(\s*):(\s*)', line)
        if not m:
            return None
        before = m.group(1)
        after = line[m.end():]
        colon = ':'
        after_colon = ' ' if space_after_colon else ''
        new_line = f'{before}{colon}{after_colon}{after}'
        if new_line != line:
            return new_line
        return None

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        '''
        Check if line is a conditional directive.
        Args:
            line: The line to check
        Returns:
            True if this is a conditional directive
        '''
        # Typical make conditionals: ifdef, ifndef, ifeq, ifneq, else, endif
        return bool(re.match(r'^\s*(ifeq|ifneq|ifdef|ifndef|else|endif)\b', line))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        '''
        Get the appropriate indentation level for conditional directives.
        Args:
            line: The conditional directive line
        Returns:
            Number of spaces for indentation
        '''
        # For demonstration, let's use 0 for top-level, 2 for nested
        # Count the number of leading spaces/tabs
        m = re.match(r'^(\s*)', line)
        if m:
            return len(m.group(1).replace('\t', '  '))
        return 0
