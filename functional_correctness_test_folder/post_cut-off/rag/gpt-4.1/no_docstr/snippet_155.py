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
        # Match =, :=, +=, ?=, !=, etc. but not == or inside quotes
        # Exclude ==, <=, >=, != (comparison), but include :=, +=, ?=, != (make)
        # For Makefiles, assignment ops: =, :=, +=, ?=, !=
        return bool(re.search(r'(?<![<>=!])\s*(?:\+|\?|:|!)?=\s*', line))

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
        # Assignment ops: =, :=, +=, ?=, !=
        def replacer(match):
            op = match.group(1)
            if use_spaces:
                return f' {op} '
            else:
                return op
        # Pattern: (\+|:|\?|!)?=, not preceded by <, >, =, ! (to avoid ==, >=, etc)
        pattern = r'(?<![<>=!])\s*(\+?|\:?|\!?|\??)=\s*'
        # Only replace the first occurrence
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
        # Only operate if line looks like a target definition: target: deps
        # Don't match pattern rules (with %), or variable assignments
        if ':' not in line or re.match(r'\s*#', line):
            return None
        # Exclude lines with assignment operators before colon
        if re.search(r'(?<![<>=!])\s*(?:\+|\?|:|!)?=\s*', line):
            return None
        # Exclude pattern rules (with % before colon)
        if re.search(r'%\s*:', line):
            return None
        # Find the first colon not in quotes
        # Split at first colon
        parts = line.split(':', 1)
        if len(parts) != 2:
            return None
        left, right = parts
        left_strip = left.rstrip()
        right_strip = right.lstrip()
        before = ' ' if space_before else ''
        after = ' ' if space_after else ''
        new_line = f"{left_strip}{before}:{after}{right_strip}"
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
        # Pattern rules: %.o: %.c
        # Only operate if % appears before colon
        m = re.match(r'^(\s*[^:=\s][^:=]*%[^:=]*?)\s*:\s*(.*)$', line)
        if not m:
            return None
        left = m.group(1).rstrip()
        right = m.group(2).lstrip()
        after = ' ' if space_after_colon else ''
        new_line = f"{left}:{after}{right}"
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
        # Makefile conditionals: ifdef, ifndef, ifeq, ifneq, else, endif
        return bool(re.match(r'^\s*(ifdef|ifndef|ifeq|ifneq|else|endif)\b', line))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        '''
        Get the appropriate indentation level for conditional directives.
        Args:
            line: The conditional directive line
        Returns:
            Number of spaces for indentation
        '''
        # Simple heuristic: 0 for if*, else, endif at top-level
        # Indent by 2 for nested conditionals (count number of if* before this line minus endif)
        # For this utility, just return 0 for top-level, 2 for else, 0 for endif
        # (A real implementation would need context)
        line = line.lstrip()
        if line.startswith('else'):
            return 2
        elif line.startswith('endif'):
            return 0
        elif line.startswith(('ifdef', 'ifndef', 'ifeq', 'ifneq')):
            return 0
        return 0
