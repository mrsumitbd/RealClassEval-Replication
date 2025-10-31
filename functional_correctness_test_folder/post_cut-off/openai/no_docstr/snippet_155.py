
import re
from typing import Optional


class PatternUtils:
    """
    Utility class for handling simple pattern and assignment formatting.
    """

    @staticmethod
    def contains_assignment(line: str) -> bool:
        """
        Return True if the line contains an assignment operator (=) that is not part of
        a comparison or other multi-character operator.
        """
        # Matches a single '=' that is not preceded or followed by '=', '!', '<', '>', or ':'.
        return bool(re.search(r'(?<![=!<>:])=(?!=)', line))

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        """
        Ensure that the assignment operator has the requested spacing.
        If use_spaces is True, there will be exactly one space before and after '='.
        If False, there will be no spaces around '='.
        """
        if use_spaces:
            # Replace any amount of whitespace around '=' with a single space on each side
            return re.sub(r'\s*=\s*', ' = ', line)
        else:
            # Remove all whitespace around '='
            return re.sub(r'\s*=\s*', '=', line)

    @staticmethod
    def format_target_colon(line: str, space_before: bool = False, space_after: bool = True) -> Optional[str]:
        """
        Format a colon that is used as a target separator (e.g., in a dictionary or
        pattern). The colon will be surrounded by spaces according to the flags.
        Returns None if no colon is found that is not part of a multi-character operator.
        """
        # Find a colon that is not part of '::' or '=>'
        match = re.search(r'(?<![:=])(:)(?![:=])', line)
        if not match:
            return None

        before = ' ' if space_before else ''
        after = ' ' if space_after else ''
        formatted = before + ':' + after
        return re.sub(r'(?<![:=])(:)(?![:=])', formatted, line, count=1)

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        """
        Format a pattern rule line that contains a colon. Ensures that there is a
        single space after the colon if space_after_colon is True, otherwise removes
        any space after the colon. The colon must not be part of a multi-character
        operator.
        """
        # Find a colon that is not part of '::' or '=>'
        match = re.search(r'(?<![:=])(:)(?![:=])', line)
        if not match:
            return None

        if space_after_colon:
            replacement = ': '
        else:
            replacement = ':'
        return re.sub(r'(?<![:=])(:)(?![:=])', replacement, line, count=1)

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        """
        Detect if the line starts with a conditional directive such as
        '#if', '#elif', '#else', '#endif', 'if', 'elif', 'else', or 'endif'.
        Leading whitespace is ignored.
        """
        stripped = line.lstrip()
        return bool(re.match(r'^(#?(if|elif|else|endif))\b', stripped))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        """
        Return the number of leading spaces before a conditional directive.
        If the line does not contain a conditional directive, returns 0.
        """
        if not PatternUtils.is_conditional_directive(line):
            return 0
        return len(line) - len(line.lstrip(' '))
