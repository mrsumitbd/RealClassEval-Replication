
import typing


class WebVTTCommentBlock:
    '''Representation of a comment block.'''

    def __init__(self, text: str):
        '''
        Initialize.
        :param text: comment text
        '''
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        '''
        Validate the lines for a match of a comment block.
        :param lines: the lines to be validated
        :returns: true for a matching comment block
        '''
        if not lines:
            return False
        # The first line must start with "NOTE"
        if not lines[0].startswith("NOTE"):
            return False
        # A comment block must end with an empty line
        return lines[-1] == ""

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTCommentBlock':
        '''
        Create a `WebVTTCommentBlock` from lines of text.
        :param lines: the lines of text
        :returns: `WebVTTCommentBlock` instance
        '''
        lines = list(lines)
        if not lines:
            raise ValueError("No lines provided for comment block")
        # Remove the trailing empty line if present
        if lines[-1] == "":
            lines = lines[:-1]
        # Strip the "NOTE" keyword from the first line
        first_line = lines[0]
        if first_line.startswith("NOTE"):
            first_line = first_line[4:]  # remove "NOTE"
            if first_line.startswith(" "):
                first_line = first_line[1:]
        else:
            raise ValueError("First line does not start with NOTE")
        # Combine the first line with the rest
        comment_text = first_line
        if len(lines) > 1:
            comment_text += "\n" + "\n".join(lines[1:])
        return cls(comment_text)

    @staticmethod
    def format_lines(lines: str) -> typing.List[str]:
        '''
        Return the lines for a comment block.
        :param lines: comment lines
        :returns: list of lines for a comment block
        '''
        parts = lines.splitlines()
        if not parts:
            return ["NOTE", ""]
        first = parts[0]
        rest = parts[1:]
        formatted = [f"NOTE {first}"] + rest + [""]
        return formatted
