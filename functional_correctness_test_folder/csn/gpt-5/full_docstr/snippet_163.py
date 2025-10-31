import typing


class WebVTTStyleBlock:
    '''Representation of a style block.'''

    def __init__(self, text: str):
        '''
        Initialize.
        :param text: style text
        '''
        self.text = '' if text is None else str(text)

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        '''
        Validate the lines for a match of a style block.
        :param lines: the lines to be validated
        :returns: true for a matching style block
        '''
        if not lines:
            return False
        first = lines[0].strip()
        if first != "STYLE":
            return False
        # Require at least one content line after the STYLE header
        return len(lines) >= 2

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':
        '''
        Create a `WebVTTStyleBlock` from lines of text.
        :param lines: the lines of text
        :returns: `WebVTTStyleBlock` instance
        '''
        raw = [l.rstrip('\n\r') for l in lines]
        if raw and raw[0].strip() == "STYLE":
            raw = raw[1:]
        # Remove trailing empty line(s) that typically terminate a block
        while raw and raw[-1] == '':
            raw.pop()
        text = '\n'.join(raw)
        return cls(text)

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        '''
        Return the lines for a style block.
        :param lines: style lines
        :returns: list of lines for a style block
        '''
        if lines is None:
            content = []
        else:
            # Normalize: ensure pure content (no header), strip line endings
            content = []
            for l in lines:
                s = '' if l is None else str(l)
                content.append(s.rstrip('\n\r'))
            # Remove trailing empty strings to avoid duplicating terminator
            while content and content[-1] == '':
                content.pop()
        return ["STYLE", *content, ""]
