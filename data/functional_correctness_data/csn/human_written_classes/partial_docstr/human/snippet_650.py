from hgvs.exceptions import HGVSInvalidIntervalError

class IntervalPair:
    """Represents a match, insertion, or deletion segment of an
    alignment. If a match, the lengths must be equal; if an insertion or
    deletion, the length of the ref or tgt must be zero respectively."""
    __slots__ = ('ref', 'tgt')

    def __init__(self, ref, tgt):
        if not (ref.len == tgt.len or (ref.len == 0 and tgt.len != 0) or (ref.len != 0 and tgt.len == 0)):
            raise HGVSInvalidIntervalError("IntervalPair doesn't represent a match, insertion, or deletion")
        self.ref = ref
        self.tgt = tgt

    def __repr__(self):
        return '{self.__class__.__name__}(ref={self.ref},tgt={self.tgt})'.format(self=self)