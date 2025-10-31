
from typing import Optional


class PatternUtils:
    @staticmethod
    def contains_assignment(line: str) -> bool:
        """
        Return True if the line contains an assignment operator '=' that is not part of a comment.
        """
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            return False
        # Ignore variable references like $(VAR) or ${VAR}
        # A simple heuristic: if '=' is present and not surrounded by '$(' or '${'
        return "=" in line and not line.lstrip().startswith(("$( ", "${"))

    @staticmethod
    def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
        """
        Adjust spacing around the assignment operator.
        If use_spaces is True, ensure exactly one space before and after '='.
        If False, remove all spaces around '='.
        """
        if not PatternUtils.contains_assignment(line):
            return line

        # Split on the first '=' that is not part of a comment
        parts = line.split("=", 1)
        left, right = parts[0], parts[1]

        # Remove leading/trailing spaces from left and right
        left = left.rstrip()
        right = right.lstrip()

        if use_spaces:
            return f"{left} = {right}"
        else:
            return f"{left}={right}"

    @staticmethod
    def format_target_colon(
        line: str, space_before: bool = False, space_after: bool = True
    ) -> Optional[str]:
        """
        Format colon spacing in target definitions.
        """
        stripped = line.strip()
        if not stripped or ":" not in stripped:
            return None

        # Find the first colon that separates target from prerequisites
        idx = stripped.find(":")
        target = stripped[:idx].rstrip()
        rest = stripped[idx + 1:].lstrip()

        new_colon = ":"
        if space_before:
            new_colon = f" {new_colon}"
        if space_after:
            new_colon = f"{new_colon} "

        new_line = f"{target}{new_colon}{rest}"
        if new_line == line:
            return None
        return new_line

    @staticmethod
    def format_pattern_rule(line: str, space_after_colon: bool = True) -> Optional[str]:
        """
        Format pattern rule spacing after the colon.
        """
        stripped = line.strip()
        if not stripped or ":" not in stripped:
            return None

        idx = stripped.find(":")
        left = stripped[:idx].rstrip()
        right = stripped[idx + 1:].lstrip()

        if space_after_colon:
            right = f" {right}" if not right.startswith(" ") else right
        else:
            right = right.lstrip()

        new_line = f"{left}:{right}"
        if new_line == line:
            return None
        return new_line

    @staticmethod
    def is_conditional_directive(line: str) -> bool:
        """
        Return True if the line is a Makefile conditional directive.
        """
        stripped = line.lstrip()
        directives = ("ifeq", "ifneq", "ifdef", "ifndef", "else", "endif")
        return stripped.startswith(directives)

    @staticmethod
    def get_conditional_indent_level(line: str) -> int:
        """
        Return the indentation level (number of spaces) for a conditional directive.
        For conditional directives, the indentation level is 0.
        """
        if PatternUtils.is_conditional_directive(line):
            return 0
        return 0
