from typing import Iterable, List, Sequence


class WebVTTCommentBlock:
    '''Representation of a comment block.'''

    def __init__(self, text: str):
        '''
        Initialize.
        :param text: comment text
        '''
        self.text = text if text is not None else ""

    @classmethod
    def is_valid(cls, lines: Sequence[str]) -> bool:
        '''
        Validate the lines for a match of a comment block.
        :param lines: the lines to be validated
        :returns: true for a matching comment block
        '''
        if not lines:
            return False
        first = lines[0]
        if not isinstance(first, str):
            return False
        # Must start with "NOTE" and either end there or followed by whitespace
        if not (first.startswith("NOTE") and (len(first) == 4 or first[4].isspace())):
            return False
        # No empty line inside the block (empty line would terminate a NOTE block)
        for line in lines[1:]:
            if line == "":
                return False
        return True

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> 'WebVTTCommentBlock':
        '''
        Create a `WebVTTCommentBlock` from lines of text.
        :param lines: the lines of text
        :returns: `WebVTTCommentBlock` instance
        '''
        lst = list(lines)
        if not cls.is_valid(lst):
            raise ValueError("Invalid NOTE block lines")
        first = lst[0]
        # Extract inline comment after NOTE (allow any whitespace after NOTE)
        if len(first) > 4 and first[4].isspace():
            # Keep the remainder as-is but strip only the first whitespace char
            # after NOTE; if multiple whitespace characters, we remove only one.
            remainder = first[5:] if len(
                first) > 5 and first[4] == " " else first[4:].lstrip()
            content_lines = [remainder] if remainder != "" else []
        else:
            content_lines = []
        if len(lst) > 1:
            content_lines.extend(lst[1:])
        text = "\n".join(content_lines)
        return cls(text)

    @staticmethod
    def format_lines(lines: str) -> List[str]:
        '''
        Return the lines for a comment block.
        :param lines: comment lines
        :returns: list of lines for a comment block
        '''
        text = "" if lines is None else lines
        parts = text.splitlines()
        if not parts:
            return ["NOTE"]
        if len(parts) == 1:
            return ["NOTE " + parts[0]] if parts[0] != "" else ["NOTE"]
        return ["NOTE"] + parts
