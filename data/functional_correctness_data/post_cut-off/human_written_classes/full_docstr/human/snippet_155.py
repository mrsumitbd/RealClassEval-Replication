import re
from typing import Optional

class PatternUtils:
    """Common pattern matching utilities used across formatting rules."""
    ASSIGNMENT_PATTERNS = {'spaced': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1 := \\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1 += \\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1 ?= \\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1 = \\2')], 'compact': [('^([^:+=?!]*?)\\s*:=\\s*(.*)', '\\1:=\\2'), ('^([^:+=?!]*?)\\s*\\+=\\s*(.*)', '\\1+=\\2'), ('^([^:+=?!]*?)\\s*\\?=\\s*(.*)', '\\1?=\\2'), ('^([^:+=?!]*?)\\s*=\\s*(.*)', '\\1=\\2')]}

    @staticmethod
    def contains_assignment(line: str) -> bool:
        """
        Check if line contains an assignment operator.

        Args:
            line: The line to check

        Returns:
            True if line contains assignment operators
        """
        stripped = line.strip()
        if stripped.startswith(('export ', 'unexport ')):
            return False
        return bool(re.search('[^:+=?!<>]*[=]', line) and (not re.search('[!<>=]=', line)))

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool=True) -> str:
        """
        Apply consistent spacing around assignment operators.

        Args:
            line: The line to format
            use_spaces: Whether to use spaces around operators

        Returns:
            The formatted line
        """
        patterns = PatternUtils.ASSIGNMENT_PATTERNS['spaced' if use_spaces else 'compact']
        for pattern, replacement in patterns:
            new_line = re.sub(pattern, replacement, line)
            if new_line != line:
                return new_line
        return line

    @staticmethod
    def format_target_colon(line: str, space_before: bool=False, space_after: bool=True) -> Optional[str]:
        """
        Format colon spacing in target definitions.

        Args:
            line: The line to format
            space_before: Whether to add space before colon
            space_after: Whether to add space after colon

        Returns:
            Formatted line or None if no changes needed
        """
        if line.startswith('\t'):
            return None
        if ':' in line and (not line.strip().startswith(('if', 'else', 'endif', 'define', 'endef'))) and (not re.search('[=]', line)) and (not re.search('%.*:', line)) and (line.count(':') == 1):
            colon_match = re.match('^(\\s*)([^:]+):(.*)$', line)
            if colon_match:
                leading_whitespace = colon_match.group(1)
                target_part = colon_match.group(2)
                deps_part = colon_match.group(3)
                if space_before:
                    target_part = target_part.rstrip() + ' '
                else:
                    target_part = target_part.rstrip()
                if space_after:
                    if deps_part.strip():
                        deps_part = ' ' + ' '.join(deps_part.split())
                    else:
                        deps_part = ''
                else:
                    deps_part = ' '.join(deps_part.split()) if deps_part.strip() else ''
                new_line = leading_whitespace + target_part + ':' + deps_part
                if new_line != line:
                    return new_line
        return None

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool=True) -> Optional[str]:
        """
        Format spacing in pattern rules.

        Args:
            line: The line to format
            space_after_colon: Whether to add space after colon

        Returns:
            Formatted line or None if no changes needed
        """
        if re.search('.*:\\s*%.*\\s*:\\s*', line) and (not re.search('[=]', line)):
            static_pattern_match = re.match('^(\\s*)([^:]+):\\s*([^:]+)\\s*:\\s*(.*)$', line)
            if static_pattern_match:
                leading_whitespace = static_pattern_match.group(1)
                targets_part = static_pattern_match.group(2).rstrip()
                pattern_part = static_pattern_match.group(3).strip()
                prereqs_part = static_pattern_match.group(4).strip()
                new_line = leading_whitespace + f'{targets_part}: {pattern_part}: {prereqs_part}'
                if new_line != line:
                    return new_line
        elif re.search('%.*:', line) and line.count(':') == 1:
            pattern_match = re.match('^(\\s*)([^:]+):(.*)$', line)
            if pattern_match:
                leading_whitespace = pattern_match.group(1)
                pattern_part = pattern_match.group(2)
                prereqs_part = pattern_match.group(3)
                pattern_part = pattern_part.rstrip()
                if space_after_colon:
                    if prereqs_part.startswith(' '):
                        prereqs_part = ' ' + prereqs_part.lstrip()
                    elif prereqs_part:
                        prereqs_part = ' ' + prereqs_part
                else:
                    prereqs_part = prereqs_part.lstrip()
                new_line = leading_whitespace + pattern_part + ':' + prereqs_part
                if new_line != line:
                    return new_line
        return None

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        """
        Check if line is a conditional directive.

        Args:
            line: The line to check

        Returns:
            True if this is a conditional directive
        """
        stripped = line.strip()
        return stripped.startswith(('ifeq', 'ifneq', 'ifdef', 'ifndef', 'else', 'endif'))

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        """
        Get the appropriate indentation level for conditional directives.

        Args:
            line: The conditional directive line

        Returns:
            Number of spaces for indentation
        """
        stripped = line.strip()
        if stripped.startswith(('ifeq', 'ifneq', 'ifdef', 'ifndef')):
            return 0
        elif stripped.startswith('else') or stripped.startswith('endif'):
            return 0
        else:
            return 2