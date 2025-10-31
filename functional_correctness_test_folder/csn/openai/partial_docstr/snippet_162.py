
import typing


class WebVTTCommentBlock:
    """
    Represents a WebVTT comment block.
    """

    def __init__(self, text: str):
        """
        Initialise a comment block with the given text.
        :param text: The comment text (without the leading NOTE keyword).
        """
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        """
        Validate the lines for a match of a comment block.
        :param lines: the lines to be validated
        :returns: true for a matching comment block
        """
        if not lines:
            return False

        first = lines[0]
        # Must start with NOTE and either be exactly "NOTE" or "NOTE " followed by text
        if not first.startswith("NOTE"):
            return False
        if len(first) > 4 and first[4] != " ":
            return False

        # Must end with an empty line
        if lines[-1] != "":
            return False

        # All lines between the first and the last must not be empty
        for line in lines[1:-1]:
            if line == "":
                return False

        return True

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> "WebVTTCommentBlock":
        """
        Create a `WebVTTCommentBlock` from lines of text.
        :param lines: the lines of text
        :returns: `WebVTTCommentBlock` instance
        """
        lines = list(lines)
        if not cls.is_valid(lines):
            raise ValueError(
                "Provided lines do not form a valid WebVTT comment block")

        # Extract comment text
        first = lines[0]
        comment = first[4:].lstrip()  # remove "NOTE" and leading whitespace
        for line in lines[1:-1]:
            comment += "\n" + line

        return cls(comment)

    @staticmethod
    def format_lines(lines: str) -> typing.List[str]:
        """
        Return the lines for a comment block.
        :param lines: comment lines
        :returns: list of lines for a comment block
        """
        # Split the comment into individual lines
        parts = lines.splitlines()
        if not parts:
            # Empty comment
            return ["NOTE", ""]
        # First line: NOTE + first part
        first_line = "NOTE " + parts[0]
        # Remaining lines
        result = [first_line] + parts[1:] + [""]
        return result
