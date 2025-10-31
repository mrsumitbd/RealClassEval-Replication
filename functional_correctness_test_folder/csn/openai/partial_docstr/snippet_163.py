
import typing


class WebVTTStyleBlock:
    """
    Represents a WebVTT style block.
    """

    def __init__(self, text: str):
        """
        Initialise the style block with the raw text.
        """
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        """
        Determine whether the supplied lines form a valid WebVTT style block.
        A minimal valid block must start with the keyword 'STYLE' (case‑insensitive)
        and contain at least one additional line.
        """
        if not lines:
            return False
        # The first line must be exactly 'STYLE' (ignoring surrounding whitespace)
        first = lines[0].strip()
        if first.upper() != "STYLE":
            return False
        # There must be at least one more line after the header
        return len(lines) > 1

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':
        """
        Create a WebVTTStyleBlock from an iterable of lines.
        The lines are joined with a newline character to form the block text.
        """
        # Convert to a list to allow multiple passes
        line_list = list(lines)
        if not cls.is_valid(line_list):
            raise ValueError(
                "Provided lines do not form a valid WebVTT style block.")
        # Join lines preserving the original line breaks
        block_text = "\n".join(line.rstrip("\n") for line in line_list)
        return cls(block_text)

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        """
        Format a list of lines for a WebVTT style block.
        Strips leading/trailing whitespace from each line and ensures each line
        ends with a single newline character when joined later.
        """
        return [line.strip() for line in lines]
