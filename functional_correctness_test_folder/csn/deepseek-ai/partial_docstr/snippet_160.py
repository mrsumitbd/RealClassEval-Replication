
import typing


class SBVCueBlock:
    '''Representation of a cue timing block.'''

    def __init__(self, start: str, end: str, payload: typing.Sequence[str]):
        self.start = start
        self.end = end
        self.payload = payload

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if len(lines) < 2:
            return False
        first_line = lines[0].strip()
        if '-->' not in first_line:
            return False
        parts = first_line.split('-->')
        if len(parts) != 2:
            return False
        start, end = parts[0].strip(), parts[1].strip()
        return bool(start and end)

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        '''
        Create a `SBVCueBlock` from lines of text.
        :param lines: the lines of text
        :returns: `SBVCueBlock` instance
        '''
        if not cls.is_valid(lines):
            raise ValueError("Invalid cue block lines")
        first_line = lines[0].strip()
        start, end = first_line.split('-->')
        start, end = start.strip(), end.strip()
        payload = [line.strip() for line in lines[1:]]
        return cls(start, end, payload)
