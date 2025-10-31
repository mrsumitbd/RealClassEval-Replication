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
        # Exclude lines that are comments or empty
        if not line or line.lstrip().startswith('#'):
            return False
        # Match =, :=, ?=, +=, !=, but not == or inside strings
        # Exclude ==, >=, <=, != (comparison), but allow :=, +=, ?=, != (make)
        # We'll match assignment operators used in Makefiles
        assignment_pattern = re.compile(
            r'(?<![=!<>])\b([a-zA-Z0-9_.-]+)\s*(\?|:|\+|!)?=\s*')
        return bool(assignment_pattern.search(line))

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
        # Match variable name, optional operator, and =
        pattern = re.compile(r'^(\s*[a-zA-Z0-9_.-]+)\s*(\?|:|\+|!)?=\s*')
        match = pattern.match(line)
        if not match:
            return line
        var = match.group(1)
        op = match.group(2) if match.group(2) else ''
        rest = line[match.end():]
        if use_spaces:
            spaced = f"{var} {op + '=' if op else '='} "
        else:
            spaced = f"{var}{op + '=' if op else '='}"
        return spaced + rest

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
        # Only match lines that look like target: deps
        # Don't match pattern rules (%.o: %.c)
        pattern = re.compile(r'^(\s*[\w\.\-/\$\(\)%]+)\s*:\s*(.*)$')
        match = pattern.match(line)
        if not match:
            return None
        target = match.group(1)
        deps = match.group(2)
        before = ' ' if space_before else ''
        after = ' ' if space_after else ''
        formatted = f"{target}{before}:{after}{deps}"
        if formatted == line:
            return None
        return formatted

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
        # Pattern rules: %.o: %.c or %.o: %.c %.h
        pattern = re.compile(r'^(\s*%[\w\.\-/\$\(\)]*)\s*:\s*(.*)$')
        match = pattern.match(line)
        if not match:
            return None
        target = match.group(1)
        deps = match.group(2)
        after = ' ' if space_after_colon else ''
        formatted = f"{target}: {after}{deps}" if after else f"{target}:{deps}"
        # Remove double space if present
        formatted = re.sub(r':  ', ': ', formatted)
        if formatted == line:
            return None
        return formatted

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
        pattern = re.compile(r'^\s*(ifdef|ifndef|ifeq|ifneq|else|endif)\b')
        return bool(pattern.match(line))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        '''
        Get the appropriate indentation level for conditional directives.
        Args:
            line: The conditional directive line
        Returns:
            Number of spaces for indentation
        '''
        # For Makefiles, often 0 for ifdef/ifndef/ifeq/ifneq/else/endif
        # But some style guides indent inside conditionals
        # We'll return 0 for the directive itself
        return 0
