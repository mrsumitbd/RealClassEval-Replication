from collections import defaultdict, deque

class LookaheadIterator:
    """
    Wrapper around an iterator or generator that allows for peeking
    at the nth token of any n, and the ability to skip intervening
    tokens (e.g., what is the 3rd token that is not a comment?).
    """

    def __init__(self, iterable, n=1024):
        assert n > 0
        self._iterable = iterable
        self._n = n
        self._buffer = deque()
        self._buffer_fill()

    def _buffer_fill(self, n=None):
        if n is None:
            n = self._n
        iterable = self._iterable
        buffer = self._buffer
        append = buffer.append
        for _ in range(max(n - len(buffer), 0)):
            try:
                datum = next(iterable)
                append(datum)
            except StopIteration:
                if len(buffer) == 0:
                    return False
                else:
                    break
        return True

    def next(self, skip=None):
        """
        Remove the next datum from the buffer and return it.
        """
        buffer = self._buffer
        popleft = buffer.popleft
        if skip is not None:
            while True:
                try:
                    if not skip(buffer[0]):
                        break
                    popleft()
                except IndexError:
                    if not self._buffer_fill():
                        raise StopIteration from None
        try:
            datum = popleft()
        except IndexError:
            if not self._buffer_fill():
                raise StopIteration from None
            datum = popleft()
        return datum

    def peek(self, n=0, skip=None, drop=False):
        """
        Return the *n*th datum from the buffer.
        """
        buffer = self._buffer
        popleft = buffer.popleft
        datum = None
        if skip is not None:
            stack = []
            stackpush = stack.append
            while n >= 0:
                try:
                    datum = popleft()
                except IndexError:
                    if not self._buffer_fill():
                        raise StopIteration from None
                    datum = popleft()
                if not skip(datum):
                    n -= 1
                    stackpush(datum)
                elif not drop:
                    stackpush(datum)
            buffer.extendleft(reversed(stack))
        else:
            if not self._buffer_fill(n + 1):
                raise StopIteration
            datum = buffer[n]
        return datum