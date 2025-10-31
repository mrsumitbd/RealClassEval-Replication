
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
        if not lines[0].startswith('START:') or not lines[1].startswith('END:'):
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        '''
        Create a `SBVCueBlock` from lines of text.
        :param lines: the lines of text
        :returns: `SBVCueBlock` instance
        '''
        if not cls.is_valid(lines):
            raise ValueError("Invalid lines for SBVCueBlock")
        start = lines[0].split(':')[1].strip()
        end = lines[1].split(':')[1].strip()
        payload = lines[2:]
        return cls(start, end, payload)
