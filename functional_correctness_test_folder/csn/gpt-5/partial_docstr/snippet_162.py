import typing


class WebVTTCommentBlock:

    def __init__(self, text: str):
        self.text = text or ""

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        '''
        Validate the lines for a match of a comment block.
        :param lines: the lines to be validated
        :returns: true for a matching comment block
        '''
        if not lines:
            return False
        first = lines[0].rstrip("\n\r")
        if not first.startswith("NOTE"):
            return False
        if len(first) == 4:
            return True
        return first[4].isspace()

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTCommentBlock':
        '''
        Create a `WebVTTCommentBlock` from lines of text.
        :param lines: the lines of text
        :returns: `WebVTTCommentBlock` instance
        '''
        collected = [l.rstrip("\n\r") for l in lines]
        if not cls.is_valid(collected):
            raise ValueError(
                "Lines do not represent a valid WebVTT comment block")
        first = collected[0]
        rest = collected[1:]
        if len(first) == 4:
            text = "\n".join(rest)
        else:
            initial = first[4:].lstrip()
            if rest:
                text = initial + ("\n" if initial else "") + \
                    "\n".join(rest) if any(rest) else initial
            else:
                text = initial
        return cls(text)

    @staticmethod
    def format_lines(lines: str) -> typing.List[str]:
        '''
        Return the lines for a comment block.
        :param lines: comment lines
        :returns: list of lines for a comment block
        '''
        if lines is None:
            return ["NOTE"]
        parts = str(lines).splitlines()
        if not parts:
            return ["NOTE"]
        first = parts[0]
        if first:
            header = "NOTE " + first
        else:
            header = "NOTE"
        return [header] + parts[1:]
