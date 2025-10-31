from hgvs.exceptions import HGVSInvalidIntervalError

class Interval:
    """Represents a segment of a sequence in interbase
    coordinates (0-based, right-open).
    """
    __slots__ = ('start_i', 'end_i')

    def __init__(self, start_i, end_i):
        if not start_i <= end_i:
            raise HGVSInvalidIntervalError('start_i must be less than or equal to end_i')
        self.start_i = start_i
        self.end_i = end_i

    @property
    def len(self):
        return self.end_i - self.start_i

    def __repr__(self):
        return '{self.__class__.__name__}(start_i={self.start_i},end_i={self.end_i})'.format(self=self)