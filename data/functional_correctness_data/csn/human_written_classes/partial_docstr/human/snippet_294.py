from secrets import randbelow, token_bytes
from sys import maxsize as MaxInt
from random import Random

class NUID:
    """
    NUID is an implementation of the approach for fast generation of
    unique identifiers used for inboxes in NATS.
    """

    def __init__(self) -> None:
        self._prand = Random(randbelow(MaxInt))
        self._seq = self._prand.randint(0, MAX_SEQ)
        self._inc = MIN_INC + self._prand.randint(BASE + 1, INC)
        self._prefix = bytearray()
        self.randomize_prefix()

    def next(self) -> bytearray:
        """
        next returns the next unique identifier.
        """
        self._seq += self._inc
        if self._seq >= MAX_SEQ:
            self.randomize_prefix()
            self.reset_sequential()
        l = self._seq
        prefix = self._prefix[:]
        suffix = bytearray(SEQ_LENGTH)
        for i in reversed(range(SEQ_LENGTH)):
            suffix[i] = DIGITS[int(l) % BASE]
            l //= BASE
        prefix.extend(suffix)
        return prefix

    def randomize_prefix(self) -> None:
        random_bytes = token_bytes(PREFIX_LENGTH)
        self._prefix = bytearray((DIGITS[c % BASE] for c in random_bytes))

    def reset_sequential(self) -> None:
        self._seq = self._prand.randint(0, MAX_SEQ)
        self._inc = MIN_INC + self._prand.randint(0, INC)