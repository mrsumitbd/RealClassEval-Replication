
import typing


class WebVTTStyleBlock:
    """
    A minimal representation of a WebVTT style block.

    The block is expected to start with a line that begins with the keyword
    ``STYLE`` (case‑insensitive) and to contain at least one CSS rule
    enclosed in braces.  The class provides helpers to validate a sequence
    of lines, to construct an instance from an iterable of lines, and to
    format a list of lines for output.
    """

    def __init__(self, text: str):
        """
        Initialise the style block with the raw text representation.

        Parameters
        ----------
        text : str
            The raw text of the style block, including line breaks.
        """
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        """
        Determine whether the supplied lines form a valid WebVTT style block.

        A block is considered valid if:
        * The first non‑empty line starts with ``STYLE`` (case‑insensitive).
        * The block contains at least one opening ``{`` and one closing ``}``.
        * The number of opening and closing braces match.

        Parameters
        ----------
        lines : Sequence[str]
            The lines to validate.

        Returns
        -------
        bool
            ``True`` if the lines form a valid style block, otherwise ``False``.
        """
        if not lines:
            return False

        # Find the first non‑empty line
        first_line = None
        for line in lines:
            if line.strip():
                first_line = line.strip()
                break
        if first_line is None or not first_line.upper().startswith("STYLE"):
            return False

        # Count braces
        open_braces = 0
        close_braces = 0
        for line in lines:
            open_braces += line.count("{")
            close_braces += line.count("}")

        return open_braces > 0 and close_braces > 0 and open_braces == close_braces

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':
        """
        Create a ``WebVTTStyleBlock`` instance from an iterable of lines.

        Parameters
        ----------
        lines : Iterable[str]
            The lines that make up the style block.

        Returns
        -------
        WebVTTStyleBlock
            The constructed instance.
        """
        # Join lines with a newline to preserve the original formatting
        text = "\n".join(lines)
        return cls(text)

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        """
        Format a list of lines for output.

        The formatting rules are:
        * Strip leading and trailing whitespace from each line.
        * Remove any empty lines.
        * Ensure that each line ends with a single newline character
          (the caller is responsible for joining them if needed).

        Parameters
        ----------
        lines : List[str]
            The lines to format.

        Returns
        -------
        List[str]
            The formatted lines.
        """
        formatted = []
        for line in lines:
            stripped = line.strip()
            if stripped:
                formatted.append(stripped)
        return formatted
