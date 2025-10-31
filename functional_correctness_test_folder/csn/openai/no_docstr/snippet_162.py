
import typing


class WebVTTCommentBlock:
    """
    Represents a WebVTT comment block.

    A comment block starts with a line beginning with ``NOTE`` and ends with an empty line.
    The text of the comment is the content after ``NOTE`` on the first line followed by
    any subsequent lines until the terminating empty line.
    """

    def __init__(self, text: str):
        """
        Create a comment block from the given text.

        Parameters
        ----------
        text : str
            The comment text. Leading and trailing whitespace is stripped.
        """
        self.text = text.strip()

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        """
        Check whether the given sequence of lines represents a valid WebVTT comment block.

        A valid block must:
        * start with a line that begins with ``NOTE`` (case-sensitive)
        * end with an empty line

        Parameters
        ----------
        lines : Sequence[str]
            The lines to validate.

        Returns
        -------
        bool
            ``True`` if the lines form a valid comment block, ``False`` otherwise.
        """
        if not lines:
            return False
        # Must start with NOTE
        if not lines[0].startswith("NOTE"):
            return False
        # Must end with an empty line
        if lines[-1] != "":
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> "WebVTTCommentBlock":
        """
        Construct a ``WebVTTCommentBlock`` from an iterable of lines.

        Parameters
        ----------
        lines : Iterable[str]
            The lines that make up the comment block.

        Returns
        -------
        WebVTTCommentBlock
            The constructed comment block.

        Raises
        ------
        ValueError
            If the provided lines do not form a valid comment block.
        """
        lines = list(lines)
        if not cls.is_valid(lines):
            raise ValueError(
                "Provided lines do not form a valid WebVTT comment block")

        # Extract the comment text
        first_line = lines[0]
        # Remove the leading "NOTE" and any following whitespace
        comment_start = first_line[4:].lstrip()
        # Remaining comment lines (excluding the terminating empty line)
        remaining = lines[1:-1]
        if remaining:
            comment_text = comment_start + "\n" + "\n".join(remaining)
        else:
            comment_text = comment_start

        return cls(comment_text)

    @staticmethod
    def format_lines(lines: str) -> typing.List[str]:
        """
        Format a comment string into the list of lines that represent a WebVTT comment block.

        Parameters
        ----------
        lines : str
            The comment text to format.

        Returns
        -------
        List[str]
            The formatted lines, including the terminating empty line.
        """
        # Split the input into individual lines
        parts = lines.splitlines()
        if not parts:
            # Empty comment block
            return ["NOTE", ""]
        # First line after NOTE
        first = parts[0]
        rest = parts[1:]
        # Build the block
        block = ["NOTE" + (" " + first if first else "")]
        block.extend(rest)
        block.append("")  # terminating empty line
        return block
