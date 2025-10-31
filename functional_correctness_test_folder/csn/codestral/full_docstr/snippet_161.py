
import typing


class SRTCueBlock:
    '''Representation of a cue timing block.'''

    def __init__(self, index: str, start: str, end: str, payload: typing.Sequence[str]):
        '''
        Initialize.
        :param start: start time
        :param end: end time
        :param payload: caption text
        '''
        self.index = index
        self.start = start
        self.end = end
        self.payload = payload

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        '''
        Validate the lines for a match of a cue time block.
        :param lines: the lines to be validated
        :returns: true for a matching cue time block
        '''
        if len(lines) < 3:
            return False

        # Check if the first line is a valid index
        if not lines[0].strip().isdigit():
            return False

        # Check if the second line is a valid time block
        time_block = lines[1].strip()
        if '-->' not in time_block:
            return False

        start, end = time_block.split('-->')
        if not (cls._is_valid_time(start.strip()) and cls._is_valid_time(end.strip())):
            return False

        # Check if the remaining lines are valid payload
        for line in lines[2:]:
            if not line.strip():
                return False

        return True

    @classmethod
    def _is_valid_time(cls, time_str: str) -> bool:
        '''
        Validate the time string.
        :param time_str: the time string to be validated
        :returns: true for a valid time string
        '''
        parts = time_str.split(':')
        if len(parts) != 3:
            return False

        try:
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2].replace(',', '.'))
        except ValueError:
            return False

        if not (0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60):
            return False

        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        '''
        Create a `SRTCueBlock` from lines of text.
        :param lines: the lines of text
        :returns: `SRTCueBlock` instance
        '''
        if not cls.is_valid(lines):
            raise ValueError("Invalid lines for creating SRTCueBlock")

        index = lines[0].strip()
        time_block = lines[1].strip()
        start, end = time_block.split('-->')
        payload = [line.strip() for line in lines[2:]]

        return cls(index, start.strip(), end.strip(), payload)
